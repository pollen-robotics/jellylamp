import time
import threading

from collections import deque


class SafetyFirst(object):
    def __init__(self, lamp, freq=1.0):
        self.lamp = lamp
        self.period = 1 / freq

        self._check_t = threading.Thread(target=self._check)
        self._check_t.daemon = True
        self._check_t.start()

        self.issues = deque([], 10)

    def is_everything_okay(self):
        return not any(self.issues)

    def _check(self):
        while True:
            issue_temp = self.check_temp()
            issue_loads = self.check_loads()

            self.issues.append(issue_temp or issue_loads)
            time.sleep(1 / self.period)

    def check_temp(self, threshold=40):
        temperatures = self.lamp.get_reg('get_present_temperature')
        issue = False

        for id, temp in temperatures.items():
            if temp > threshold:
                print('Motor {} overheating (temp={})'.format(id, temp))
                issue = True

        return issue

    def check_loads(self, threshold=50):
        loads = self.lamp.get_reg('get_present_load')
        issue = False

        for id, l in loads.items():
            if abs(l) > threshold:
                print('Motor {} overloads (load={})'.format(id, l))
                issue = True

        return issue
