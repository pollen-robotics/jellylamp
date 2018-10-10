import numpy as np
import time

from jellylamp import JellyLamp

colors = 'off red green yellow blue pink cyan white'.split(' ')


if __name__ == '__main__':
    lamp = JellyLamp(
        ids_groups=(
            (1, 2, 3, 4, 5, 6, 7, 8),
            (9, 10, 11, 12, 13, 14, 15, 16),
        ),
        sync_freq=100.0,
        offsets={},
    )

    up_motors = [m for m in lamp.motors if m.id % 2 == 0]
    low_motors = [m for m in lamp.motors if m.id % 2 == 1]

    for m in up_motors:
        m.goal_position = 100

    for m in low_motors:
        m.goal_position = -125

    time.sleep(1)

    up_center, up_amp, up_freq = 50, 50, 0.25
    low_center, low_amp, low_freq = -25, 100, 0.25

    while True:
        up_pos = up_center + up_amp * np.sin(2 * np.pi * up_freq * time.time())
        low_pos = low_center + low_amp * np.sin(2 * np.pi * low_freq * (time.time() + 2))

        for i, m in enumerate(up_motors):
            # up_pos = up_center + up_amp * np.sin(2 * np.pi * up_freq * (time.time() + i / 2))
            m.goal_position = up_pos

        for i, m in enumerate(low_motors):
            # low_pos = low_center + low_amp * np.sin(2 * np.pi * low_freq * (time.time() + i / 2))
            m.goal_position = low_pos

        time.sleep(0.01)
