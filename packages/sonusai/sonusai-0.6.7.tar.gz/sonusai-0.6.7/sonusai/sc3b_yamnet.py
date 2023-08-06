# Copyright 2019 The TensorFlow Authors All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Inference for sc3b "dog,glassbreak,speech,other" YAMNet."""
from __future__ import division
from __future__ import print_function

import sys

import matplotlib.pyplot as plt
import numpy as np
import params as yamnet_params
import resampy
import soundfile as sf
import yamnet as yamnet_model


def main(argv):
    assert argv, 'Usage: inference.py <wav file> <wav file> ...'

    params = yamnet_params.Params()
    yamnet = yamnet_model.yamnet_frames_model(params)
    yamnet.load_weights('yamnet.h5')
    class_names = yamnet_model.class_names('yamnet_class_map.csv')
    # yamnet_classes = yamnet_model.class_names('yamnet_class_map.csv')

    for file_name in argv:
        # Decode the WAV file.
        wav_data, sr = sf.read(file_name, dtype=np.int16)
        assert wav_data.dtype == np.int16, 'Bad sample type: %r' % wav_data.dtype
        waveform = wav_data / 32768.0  # Convert to [-1.0, +1.0]
        waveform = waveform.astype('float32')

        # Convert to mono and the sample rate expected by YAMNet.
        if len(waveform.shape) > 1:
            waveform = np.mean(waveform, axis=1)
        if sr != params.sample_rate:
            waveform = resampy.resample(waveform, sr, params.sample_rate)

        # Predict YAMNet classes.
        scores, embeddings, spectrogram = yamnet(waveform)
        scores = scores.numpy()
        spectrogram = spectrogram.numpy()

        # Visualize the results.
        plt.figure(figsize=(10, 8))

        # Plot the waveform.
        plt.subplot(4, 1, 1)
        plt.plot(waveform)
        plt.xlim([0, len(waveform)])
        # Plot the log-mel spectrogram (returned by the model).
        plt.subplot(4, 1, 2)
        plt.imshow(spectrogram.T, aspect='auto', interpolation='nearest', origin='lower')

        # Plot and label the model output scores for the top-scoring classes.
        mean_scores = np.mean(scores, axis=0)
        top_N = 10
        top_class_indices = np.argsort(mean_scores)[::-1][:top_N]
        plt.subplot(4, 1, 3)
        plt.imshow(scores[:, top_class_indices].T, aspect='auto', interpolation='nearest', cmap='gray_r')
        # Compensate for the patch_window_seconds (0.96s) context window to align with spectrogram.
        patch_padding = (params.patch_window_seconds / 2) / params.patch_hop_seconds
        plt.xlim([-patch_padding, scores.shape[0] + patch_padding])
        # Label the top_N classes.
        yticks = range(0, top_N, 1)
        plt.yticks(yticks, [class_names[top_class_indices[x]] for x in yticks])
        _ = plt.ylim(-0.5 + np.array([top_N, 0]))

        # Plot the 3 probabilities
        sc3bclass = np.array([69, 435, 0])
        otherclass = np.arange(scores.shape[1])
        otherclass = np.delete(otherclass, sc3bclass)
        othermax = np.max(scores[:, otherclass], axis=1)
        plt.subplot(4, 1, 4)
        plt.plot(scores[:, sc3bclass])
        # plt.plot(othermax)
        plt.legend(class_names[sc3bclass], loc='best')

        # plt.show()
        # plt.savefig("fig.pdf")

        # Scores is a matrix of (time_frames, num_classes) classifier scores.
        # Average them along time to get an overall classifier output for the clip.
        prediction = np.mean(scores, axis=0)
        # Report the highest-scoring classes and their scores.
        top5_i = np.argsort(prediction)[::-1][:5]
        print(file_name, ':\n' +
              '\n'.join('  {:12s}: {:.3f}'.format(class_names[i], prediction[i])
                        for i in top5_i))

        plt.savefig("fig.pdf")


if __name__ == '__main__':
    main(sys.argv[1:])
