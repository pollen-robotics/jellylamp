import math
import time

from jellylamp import JellyLamp

if __name__ == '__main__':
    lamp = JellyLamp(
        ids_groups=(
            (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),
            (13, 14, 15, 16, 17, 18, 19, 20, 21, 22),
            (23, 24, 25, 26, 27, 28, 29, 30, 31, 32),
        ),
        sync_freq=100.0,
    )

    t0 = time.time()
    while time.time() - t0 < 30:
        p = 30 * math.sin(2 * math.pi * 0.25 * time.time())
        for m in lamp.motors:
            m.goal_position = p
        time.sleep(.01)
