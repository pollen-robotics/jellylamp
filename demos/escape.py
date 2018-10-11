import numpy as np

# from jellylamp import JellyLamp
from jellylamp.fake import FakeJellyLamp as JellyLamp

from groups import make_groups

from moves import (
    goto_rest_position,
    breathing,
    ondulate_odd_even, ondulate_half
)


def swim(lamp):
    moves = [ondulate_odd_even, ondulate_half]
    move = np.random.choice(moves)

    duration = 2 + np.random.rand() * 8
    move(lamp, duration)


if __name__ == '__main__':
    lamp = JellyLamp(
        ids_groups=(
            (1, 2, 3, 4, 5, 6, 7, 8, 25, 26, 27, 28, 29, 30, 31, 32),
            (9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24),
        ),
        sync_freq=100.0,
        offsets={},
    )
    make_groups(lamp)

    goto_rest_position(lamp)

    try:
        while True:
            breathing(lamp, duration=5 + np.random.rand() * 5)

            if np.random.rand() < 0.1:
                swim(lamp)

    except KeyboardInterrupt:
        print('Stopping...')
        goto_rest_position(lamp)
