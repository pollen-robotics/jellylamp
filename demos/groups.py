def split_up_low(motors):
    up = [m for m in motors if m.id % 2 == 0]
    low = [m for m in motors if m.id % 2 == 1]

    return up, low


def make_groups(lamp):
    lamp.up_motors, lamp.low_motors = split_up_low(lamp.motors)

    lamp.odd_tentacles = [m for m in lamp.motors if m.id % 4 in (1, 2)]
    lamp.even_tentacles = [m for m in lamp.motors if m.id % 4 in (0, 3)]
    lamp.even_up_motors, lamp.even_low_motors = split_up_low(lamp.even_tentacles)
    lamp.odd_up_motors, lamp.odd_low_motors = split_up_low(lamp.odd_tentacles)

    lamp.north_motors = lamp.motors[0:8]
    lamp.north_up_motors, lamp.north_low_motors = split_up_low(lamp.north_motors)

    lamp.east_motors = lamp.motors[8:16]
    lamp.east_up_motors, lamp.east_low_motors = split_up_low(lamp.east_motors)

    lamp.south_motors = lamp.motors[16:24]
    lamp.south_up_motors, lamp.south_low_motors = split_up_low(lamp.south_motors)

    lamp.west_motors = lamp.motors[24:32]
    lamp.west_up_motors, lamp.west_low_motors = split_up_low(lamp.west_motors)
