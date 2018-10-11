class Motor(object):
    colors = 'off red green yellow blue pink cyan white'.split(' ')

    def __init__(self, id, delegate, offset=0):
        self.id = id
        self.delegate = delegate
        self.offset = offset

        self._goal_pos = None
        self._moving_speed = None
        self._color = None

    @property
    def goal_position(self):
        return self._goal_pos

    @goal_position.setter
    def goal_position(self, new_pos):
        self._goal_pos = new_pos
        self.delegate.update_reg('pos', self.id, new_pos - self.offset)

    @property
    def moving_speed(self):
        return self._moving_speed

    @moving_speed.setter
    def moving_speed(self, new_speed):
        self._moving_speed = new_speed
        self.delegate.update_reg('speed', self.id, new_speed)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color):
        if new_color not in self.colors:
            raise ValueError('color must be one of {}'.format(self.colors))

        self._color = new_color
        self.delegate.update_reg('color', self.id, new_color)
