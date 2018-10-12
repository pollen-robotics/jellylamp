import glob
import time
import threading

import pyluos

from .auto_open import auto_open_ios
from .motor import Motor
from .slm import SoundLevelMeter


class JellyLamp(object):
    def __init__(self, ids_groups, sync_freq, offsets):
        self._ios = auto_open_ios(ids_groups)

        self._reg = {'pos': {}, 'color': {}, 'speed': {}}

        self.motors = []
        for ids, io in self._ios.items():
            for id in ids:
                offset = offsets[id] if id in offsets else 0
                m = Motor(id, delegate=self, offset=offset)
                setattr(self, 'm{}'.format(id), m)
                self.motors.append(m)
        self.motors = sorted(self.motors, key=lambda m: m.id)

        port = glob.glob('/dev/ttyUSB*')[0]
        r = pyluos.Robot(port)

        self.imu = r.Imu_mod

        self.sync_period = 1.0 / sync_freq
        self.sync_lock = threading.Lock()

        sync_t = threading.Thread(target=self._sync)
        sync_t.daemon = True
        sync_t.start()

        # self.slm = SoundLevelMeter()

    def set_limits(self):
        self.disable_motors()
        time.sleep(0.5)

        up_limits = (-50, 110)
        low_limits = (-125, 75)

        for ids, io in self._ios.items():
            io.set_angle_limit({
                id: up_limits if id % 2 == 1 else low_limits
                for id in ids
            })

    def get_reg(self, getter):
        values = {}
        for ids, io in self._ios.items():
            val = getattr(io, getter)(ids)
            for v, id in zip(val, ids):
                values[id] = v
        return values

    def disable_motors(self):
        for ids, io in self._ios.items():
            io.disable_torque(ids)

    def _sync(self):
        sync_reg = (
            ('pos', 'set_goal_position'),
            ('speed', 'set_moving_speed'),
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
