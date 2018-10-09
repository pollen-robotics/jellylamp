class Motor(object):
    def __init__(self, id, delegate):
        self.id = id
        self.delegate = delegate
        self._goal_pos = None

    @property
    def goal_position(self):
        return self._goal_pos

    @goal_position.setter
    def goal_position(self, new_pos):
        self._goal_pos = new_pos
        self.delegate._pos[self.id] = new_pos
