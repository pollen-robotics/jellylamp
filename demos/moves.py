import numpy as np
import time


def sin(center, amp, freq, phase):
    return center + amp * np.sin(2 * np.pi * freq * (time.time() + phase))


def goto_rest_position(lamp):
    print('Going to rest position.')

    for m in lamp.motors:
        m.moving_speed = 50

    time.sleep(0.25)

    for m in lamp.up_motors:
        m.goal_position = 100

    for m in lamp.low_motors:
        m.goal_position = -125

    time.sleep(3)


def breathing(lamp, duration):
    print('Start breathing for {}s.'.format(duration))
    start = time.time()

    up_center, up_amp, up_freq = 50, 50, 0.25
    low_center, low_amp, low_freq = -25, 100, 0.25

    for m in lamp.motors:
        m.color = 'cyan'

    while time.time() - start < duration:
        up_pos = sin(up_center, up_amp, up_freq, 0.0)
        low_pos = sin(low_center, low_amp, low_freq, 2.0)

        for m in lamp.up_motors:
            m.goal_position = up_pos

        for m in lamp.low_motors:
            m.goal_position = low_pos

        time.sleep(0.01)

    print('Stop breathing.')


def ondulate_odd_even(lamp, duration):
    print('Start ondulating odd/even for {}s.'.format(duration))
    start = time.time()

    up_center, up_amp, up_freq = 50, 50, 0.25

    while time.time() - start < duration:
        odd_up_pos = sin(up_center, up_amp, up_freq, 0.0)
        even_up_pos = sin(up_center, up_amp, up_freq, 2.0)

        for m in lamp.even_up_motors:
            m.goal_position = even_up_pos

        for m in lamp.odd_up_motors:
            m.goal_position = odd_up_pos

        time.sleep(0.01)

    print('Stop.')


def ondulate_half(lamp, duration):
    print('Start ondulating half/half for {}s.'.format(duration))
    start = time.time()

    up_center, up_amp, up_freq = 50, 50, 0.25

    while time.time() - start < duration:
        first_up_pos = sin(up_center, up_amp, up_freq, 0.0)
        second_up_pos = sin(up_center, up_amp, up_freq, 2.0)

        for m in lamp.north_up_motors + lamp.east_up_motors:
            m.goal_position = first_up_pos

        for m in lamp.south_up_motors + lamp.west_up_motors:
            m.goal_position = second_up_pos

        time.sleep(0.01)

    print('Stop.')
