import math
import time

from jellylamp import JellyLamp

if __name__ == '__main__':
    lamp = JellyLamp(
        # ids_groups=(
        #     (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),
        #     (13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24),
        #     (25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36),
        # ),
        ids_groups=(
            (1, 2),
            (3, 4)
        ),
        sync_freq=100.0,
    )

    t0 = time.time()
    while time.time() - t0 < 5:
        p = 30 * math.sin(2 * 3.14 * 0.25 * time.time())
        lamp.m1.goal_position = p
        lamp.m2.goal_position = 2 * p
        lamp.m3.goal_position = 2 * p
        time.sleep(.01)
