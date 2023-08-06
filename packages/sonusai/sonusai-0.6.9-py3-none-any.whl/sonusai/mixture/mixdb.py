import json
from copy import deepcopy
from dataclasses import dataclass
from os.path import exists
from os.path import splitext
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import h5py
import numpy as np

from sonusai import SonusAIError
from sonusai.mixture.dataclasses_sonusai import DataClassSonusAIMixin
from sonusai.mixture.segment import Segment


@dataclass(frozen=True)
class TruthSetting(DataClassSonusAIMixin):
    index: Optional[List[int]] = None
    function: Optional[str] = None
    config: Optional[dict] = None


TruthSettings = List[TruthSetting]

OptionalNumberStr = Optional[Union[float, int, str]]
OptionalListNumberStr = Optional[List[Union[float, int, str]]]


@dataclass
class Augmentation(DataClassSonusAIMixin):
    normalize: OptionalNumberStr = None
    pitch: OptionalNumberStr = None
    tempo: OptionalNumberStr = None
    gain: OptionalNumberStr = None
    eq1: OptionalListNumberStr = None
    eq2: OptionalListNumberStr = None
    eq3: OptionalListNumberStr = None
    lpf: OptionalNumberStr = None
    count: Optional[int] = None
    mixup: Optional[int] = 1


Augmentations = List[Augmentation]


@dataclass(frozen=True)
class TargetFile(DataClassSonusAIMixin):
    name: str
    duration: float
    truth_settings: TruthSettings
    augmentations: Optional[Augmentations] = None
    class_balancing_augmentation: Optional[Augmentation] = None


TargetFiles = List[TargetFile]


@dataclass
class AugmentedTarget(DataClassSonusAIMixin):
    target_file_index: int
    target_augmentation_index: int


AugmentedTargets = List[AugmentedTarget]


@dataclass(frozen=True)
class NoiseFile(DataClassSonusAIMixin):
    name: str
    duration: float
    augmentations: Optional[Augmentations] = None


NoiseFiles = List[NoiseFile]

ClassCount = List[int]


@dataclass
class Mixture(DataClassSonusAIMixin):
    target_file_index: List[int] = None
    noise_file_index: int = None
    noise_offset: int = None
    target_augmentation_index: List[int] = None
    noise_augmentation_index: int = None
    snr: float = None
    samples: int = None
    target_gain: List[int] = None
    class_count: ClassCount = None
    target_snr_gain: float = None
    noise_snr_gain: float = None
    i_sample_offset: Optional[int] = None
    i_frame_offset: Optional[int] = None
    o_frame_offset: Optional[int] = None


Mixtures = List[Mixture]

MixtureID = Union[str, List[int]]


@dataclass
class MixtureDatabase(DataClassSonusAIMixin):
    class_balancing: Optional[bool] = False
    class_balancing_augmentation: Optional[Augmentation] = None
    class_count: ClassCount = None
    class_labels: List[str] = None
    class_weights_threshold: List[float] = None
    exhaustive_noise: Optional[bool] = True
    feature: str = None
    feature_samples: int = None
    feature_step_samples: int = None
    first_cba_index: Optional[int] = None
    frame_size: int = None
    mixtures: Mixtures = None
    noise_augmentations: Augmentations = None
    noises: NoiseFiles = None
    num_classes: int = None
    seed: Optional[int] = 0
    snrs: List[float] = None
    target_augmentations: Augmentations = None
    targets: TargetFiles = None
    truth_mutex: bool = None
    truth_reduction_function: str = None
    truth_settings: TruthSettings = None


def mixdb_json_from_file(name: str) -> str:
    if not exists(name):
        raise SonusAIError(f'{name} does not exist')

    ext = splitext(name)[1]

    if ext == '.json':
        with open(file=name, mode='r', encoding='utf-8') as f:
            return f.read()

    if ext == '.h5':
        with h5py.File(name=name, mode='r') as f:
            return f.attrs['mixdb']

    raise SonusAIError(f'Do not know how to load mixdb from {name}')


def mixdb_from_json(data: str) -> MixtureDatabase:
    return MixtureDatabase.from_dict(json.loads(data))


def load_mixdb(name: str) -> MixtureDatabase:
    return mixdb_from_json(mixdb_json_from_file(name))


def set_mixture_offsets(mixdb: MixtureDatabase,
                        initial_i_sample_offset: int = 0,
                        initial_i_frame_offset: int = 0,
                        initial_o_frame_offset: int = 0) -> None:
    i_sample_offset = initial_i_sample_offset
    i_frame_offset = initial_i_frame_offset
    o_frame_offset = initial_o_frame_offset
    for mixid in range(len(mixdb.mixtures)):
        mixdb.mixtures[mixid].i_sample_offset = i_sample_offset
        mixdb.mixtures[mixid].i_frame_offset = i_frame_offset
        mixdb.mixtures[mixid].o_frame_offset = o_frame_offset

        i_sample_offset += get_samples_in_mixture(mixdb, mixid)
        i_frame_offset += get_transform_frames_in_mixture(mixdb, mixid)
        o_frame_offset += get_feature_frames_in_mixture(mixdb, mixid)


def get_samples_in_mixture(mixdb: MixtureDatabase, mixid: int) -> int:
    return mixdb.mixtures[mixid].samples


def get_transform_frames_in_mixture(mixdb: MixtureDatabase, mixid: int) -> int:
    return mixdb.mixtures[mixid].samples // mixdb.frame_size


def get_feature_frames_in_mixture(mixdb: MixtureDatabase, mixid: int) -> int:
    return mixdb.mixtures[mixid].samples // mixdb.feature_step_samples


def get_sample_offsets_in_mixture(mixdb: MixtureDatabase, mixid: int) -> (int, int):
    i_sample_offset = sum([sub.samples for sub in mixdb.mixtures[:mixid]])
    return i_sample_offset, i_sample_offset + mixdb.mixtures[mixid].samples


def get_transform_frame_offsets_in_mixture(mixdb: MixtureDatabase, mixid: int) -> (int, int):
    start, stop = get_sample_offsets_in_mixture(mixdb, mixid)
    return start // mixdb.frame_size, stop // mixdb.frame_size


def get_feature_frame_offsets_in_mixture(mixdb: MixtureDatabase, mixid: int) -> (int, int):
    start, stop = get_sample_offsets_in_mixture(mixdb, mixid)
    return start // mixdb.feature_step_samples, stop // mixdb.feature_step_samples


def get_class_weights_threshold(mixdb: Union[MixtureDatabase, Dict]) -> List[float]:
    """Get the class_weights_threshold from a mixture database or a config."""
    if isinstance(mixdb, dict):
        class_weights_threshold = mixdb['class_weights_threshold']
        num_classes = mixdb['num_classes']
    else:
        class_weights_threshold = mixdb.class_weights_threshold
        num_classes = mixdb.num_classes

    if not isinstance(class_weights_threshold, list):
        class_weights_threshold = [class_weights_threshold] * num_classes

    if len(class_weights_threshold) != num_classes:
        raise SonusAIError(f'invalid class_weights_threshold length: {len(class_weights_threshold)}')

    return class_weights_threshold


def get_file_frame_segments(mixdb: MixtureDatabase, mixid: MixtureID = ':') -> dict:
    _mixid = convert_mixid_to_list(mixdb, mixid)
    file_frame_segments = dict()
    for m in _mixid:
        file_frame_segments[m] = Segment(mixdb.mixtures[m].o_frame_offset,
                                         get_feature_frames_in_mixture(mixdb, m))
    return file_frame_segments


def get_offsets(mixdb: MixtureDatabase, mixid: int) -> (int, int, int):
    if mixid >= len(mixdb.mixtures) or mixid < 0:
        raise SonusAIError(f'Invalid mixid: {mixid}')

    i_sample_offset = sum([sub.samples for sub in mixdb.mixtures[:mixid]])
    i_frame_offset = i_sample_offset // mixdb.frame_size
    o_frame_offset = i_sample_offset // mixdb.feature_step_samples

    return i_sample_offset, i_frame_offset, o_frame_offset


def new_mixdb_from_mixid(mixdb: MixtureDatabase, mixid: MixtureID) -> MixtureDatabase:
    mixdb_out = deepcopy(mixdb)
    mixdb_out.mixtures = get_mixtures_from_mixid(mixdb_out, mixid)
    set_mixture_offsets(mixdb_out)

    if not mixdb_out.mixtures:
        raise SonusAIError(f'Error processing mixid: {mixid}; resulted in empty list of mixtures')

    return mixdb_out


def load_mixid(mixdb: MixtureDatabase, name: str = None) -> List[int]:
    if name is None:
        mixid = list(range(len(mixdb.mixtures)))
    else:
        if not exists(name):
            raise SonusAIError(f'{name} does not exist')

        with open(file=name, mode='r', encoding='utf-8') as f:
            mixid = json.load(f)
            if not isinstance(mixid, dict) or 'mixid' not in mixid:
                raise SonusAIError(f'Could not find ''mixid'' in {name}')
            mixid = mixid['mixid']

    return mixid


def convert_mixid_to_list(mixdb: MixtureDatabase, mixid: MixtureID = None) -> List[int]:
    mixid_out = mixid

    if mixid_out is None:
        return list(range(len(mixdb.mixtures)))

    if isinstance(mixid_out, str):
        try:
            mixid_out = eval(f'{list(range(len(mixdb.mixtures)))}[{mixid_out}]')
        except NameError:
            return []

    if not all(isinstance(x, int) and x < len(mixdb.mixtures) for x in mixid_out):
        return []

    return mixid_out


def get_mixtures_from_mixid(mixdb: MixtureDatabase, mixid: MixtureID = None) -> Mixtures:
    return [mixdb.mixtures[i] for i in convert_mixid_to_list(mixdb, mixid)]


def get_mixid_data(mixdb: MixtureDatabase,
                   mixid: MixtureID,
                   truth_f: np.ndarray,
                   predict: np.ndarray) -> (np.ndarray, np.ndarray):
    """Collect per-feature data of specified mixids from mixdb where inputs are:
       truth_f:   truth data matching mixdb (size feature_frames x num_classes)
       predict:   prediction or segsnr data (size feature_frames x ndim, where ndim > 1)

    Returns:
        truth_f_out:    np.ndarray combined truth from mixids
        predict_out:    np.ndarray combined data from mixids
    """
    num_classes = truth_f.shape[1]
    # same as num_class for prediction data, but use for segsnr too
    num_data = predict.shape[1]

    file_frame_segments = get_file_frame_segments(mixdb, mixid)
    total_frames = sum([file_frame_segments[m].length for m in file_frame_segments])
    truth_f_out = np.empty((total_frames, num_classes), dtype=np.single)
    predict_out = np.empty((total_frames, num_data), dtype=np.single)

    # Handle the special case when input data is smaller, i.e., prediction when total mixture
    # length is a non-multiple of the batch size. In this case just pad both with zeros; should
    # have negligible effect on metrics
    frame_diff = total_frames - truth_f.shape[0]
    if frame_diff > 0:
        truth_f = np.concatenate((truth_f, np.zeros((frame_diff, num_classes))))
        predict = np.concatenate((predict, np.zeros((frame_diff, num_classes))))

    start = 0
    for m in file_frame_segments:
        length = file_frame_segments[m].length
        truth_f_out[start:start + length] = truth_f[file_frame_segments[m].get_slice()]
        predict_out[start:start + length] = predict[file_frame_segments[m].get_slice()]
        start += length

    return truth_f_out, predict_out
