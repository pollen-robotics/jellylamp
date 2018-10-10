class Motor(object):
    colors = 'off red green yellow blue pink cyan white'.split(' ')

    def __init__(self, id, delegate):
        self.id = id
        self.delegate = delegate

        self._goal_pos = None
        self._color = None

    @property
    def goal_position(self):
        return self._goal_pos

    @goal_position.setter
    def goal_position(self, new_pos):
        self._goal_pos = new_pos
        self.delegate._pos[self.id] = new_pos

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color):
        if new_color not in self.colors:
            raise ValueError('color must be one of {}'.format(self.colors))

        self._color = new_color
        self.delegate._color[self.id] = new_color
