import time
import threading

from .auto_open import auto_open_ios
from .motor import Motor


class JellyLamp(object):
    def __init__(self, ids_groups, sync_freq):
        self._ios = auto_open_ios(ids_groups)

        self._pos, self._color = {}, {}

        self.motors = []
        for ids, io in self._ios.items():
            for id in ids:
                m = Motor(id, delegate=self)
                setattr(self, 'm{}'.format(id), m)
                self.motors.append(m)

        self.sync_period = 1.0 / sync_freq
        sync_t = threading.Thread(target=self._sync)
        sync_t.daemon = True
        sync_t.start()

    def _sync(self):
        while True:
            self._push_pos()
            self._push_color()

            time.sleep(self.sync_period)

    def _push_pos(self):
        for ids, io in self._ios.items():
            pos_for_ids = {
                id: self._pos[id]
                for id in ids
                if id in self._pos
            }
            if not pos_for_ids:
                return
            io.set_goal_position(pos_for_ids)
        self._pos = {}

    def _push_color(self):
        for ids, io in self._ios.items():
            color_for_ids = {
                id: self._color[id]
                for id in ids
                if id in self._color
            }
            if not color_for_ids:
                return
            io.set_LED_color(color_for_ids)
        self._color = {}
