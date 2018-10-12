import numpy as np
import time

from jellylamp import JellyLamp
# from jellylamp.fake import FakeJellyLamp as JellyLamp
from safety import SafetyFirst

from groups import make_groups

from moves import (
    goto_rest_position,
    breathing,
    ripple
)


def swim(lamp):
    moves = [ripple]
    move = np.random.choice(moves)

    duration = 2 + np.random.rand() * 8
    move(lamp, duration)


if __name__ == '__main__':
    lamp = JellyLamp(
        ids_groups=(
            (1, 2, 3, 4, 5, 6, 7, 8),
            (25, 26, 27, 28, 29, 30, 31, 32),
            (9, 10, 11, 12, 13, 14, 15, 16),
            (17, 18, 19, 20, 21, 22, 23, 24),
        ),
        sync_freq=100.0,
        offsets={},
    )
    make_groups(lamp)
    monitor = SafetyFirst(lamp)

    goto_rest_position(lamp)

    try:
        while True:
            breathing(lamp, duration=5 + np.random.rand() * 5)

            if np.random.rand() < 0.1:
                swim(lamp)

            if not monitor.is_everything_okay():
                goto_rest_position(lamp)
                lamp.disable_motors()

                for m in lamp.motors:
                    m.color = 'red'

                while max(lamp.get_reg('get_present_temperature').values()) > 39:
                    print('Waiting for everything to cool down...')
                    print('temperature: {}'.format(lamp.get_reg('get_present_temperature')))
                    print('load: {}'.format(lamp.get_reg('get_present_load')))
                    time.sleep(10)

                for m in lamp.motors:
                    m.color = 'off'

    except KeyboardInterrupt:
        print('Stopping...')
        goto_rest_position(lamp)
