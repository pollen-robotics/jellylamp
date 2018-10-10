import time
import threading

from .auto_open import auto_open_ios
from .motor import Motor
from .slm import SoundLevelMeter


class JellyLamp(object):
    def __init__(self, ids_groups, sync_freq, offsets):
        self._ios = auto_open_ios(ids_groups)

        self._reg = {'pos': {}, 'color': {}}

        self.motors = []
        for ids, io in self._ios.items():
            for id in ids:
                offset = offsets[id] if id in offsets else 0
                m = Motor(id, delegate=self, offset=offset)
                setattr(self, 'm{}'.format(id), m)
                self.motors.append(m)

        self.sync_period = 1.0 / sync_freq
        self.sync_lock = threading.Lock()

        sync_t = threading.Thread(target=self._sync)
        sync_t.daemon = True
        sync_t.start()

        self.slm = SoundLevelMeter()

    def _sync(self):
        sync_reg = (
            ('pos', 'set_goal_position'),
            ('color', 'set_LED_color'),
        )

        while True:
            for (reg, setter) in sync_reg:
                start = time.time()
                self._push_val(reg, setter)
                dt = time.time() - start

            time.sleep(max(0, self.sync_period - dt))

    def update_reg(self, reg, id, val):
        with self.sync_lock:
            self._reg[reg][id] = val

    def _push_val(self, reg, setter):
        with self.sync_lock:
            values = self._reg[reg]

            for ids, io in self._ios.items():
                val_for_ids = {
                    id: values[id]
                    for id in ids if id in values
                }
                if val_for_ids:
                    getattr(io, setter)(val_for_ids)

            values.clear()
