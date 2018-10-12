import numpy as np

from .motor import Motor


class FakeJellyLamp(object):
    def __init__(self, ids_groups, sync_freq, offsets):
        ids = sum(map(list, ids_groups), [])
        self.motors = [
            Motor(id, self)
            for id in ids
        ]

    def disable_motors(self):
        print('Motors off!')

    def update_reg(self, reg, id, val):
        pass

    def get_reg(self, temp):
        return {m.id: int(100 * np.random.rand()) for m in self.motors}
