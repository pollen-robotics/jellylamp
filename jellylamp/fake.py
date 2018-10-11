from .motor import Motor


class FakeJellyLamp(object):
    def __init__(self, ids_groups, sync_freq, offsets):
        ids = sum(map(list, ids_groups), [])
        self.motors = [
            Motor(id, self)
            for id in ids
        ]

    def update_reg(self, reg, id, val):
        pass
