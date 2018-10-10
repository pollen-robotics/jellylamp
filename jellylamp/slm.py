import numpy as np
import pyaudio
import threading

from collections import deque


class SoundLevelMeter(object):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 256
    WIN_SIZE = 200

    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )

        self.buff = deque([], self.WIN_SIZE)
        self._lazy_sl = None

        self._lock = threading.Lock()
        self._record_t = threading.Thread(target=self._read_chunks)
        self._record_t.daemon = True
        self._record_t.start()

    def _read_chunks(self):
        while True:
            data = self.stream.read(self.CHUNK)

            with self._lock:
                self.buff.append(data)
                self._lazy_sl = None

    @property
    def sound_level(self):
        with self._lock:
            if self._lazy_sl is None:
                x = b''.join(self.buff)
                x = np.frombuffer(x, dtype='int16')

                smr = np.sqrt(np.mean(np.abs(x) ** 2))
                self._lazy_sl = smr

            return self._lazy_sl
