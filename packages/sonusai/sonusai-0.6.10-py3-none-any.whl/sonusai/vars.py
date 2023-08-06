"""sonusai vars

usage: vars

options:
    -h, --help

List custom SonusAI variables.

"""

from docopt import docopt

import sonusai
from sonusai.mixture import DEFAULT_FRAME_SIZE
from sonusai.mixture import DEFAULT_NOISE
from sonusai.utils import trim_docstring


def main():
    docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    print('Custom SonusAI variables:\n')
    print(f'  ${{default_noise}}: {DEFAULT_NOISE}')
    print(f'  ${{frame_size}}:    {DEFAULT_FRAME_SIZE}')
    print()


if __name__ == '__main__':
    main()
