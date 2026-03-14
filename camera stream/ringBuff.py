import numpy as np
from multiprocessing import shared_memory
import struct

class VideoRingBuffer:

    def __init__(self, name, shape, n_frames=16, create=False):

        self.shape = shape
        self.frame_bytes = int(np.prod(shape))
        self.n_frames = n_frames

        self.slot_size = 4 + self.frame_bytes
        total_size = int(8 + self.slot_size * n_frames)

        if create:
            self.shm = shared_memory.SharedMemory(
                name=name,
                create=True,
                size=total_size
            )
        else:
            self.shm = shared_memory.SharedMemory(name=name)

        self.buf = self.shm.buf

    def _get_seq(self):
        return struct.unpack_from("Q", self.buf, 0)[0]

    def _set_seq(self, val):
        struct.pack_into("Q", self.buf, 0, val)

    def write(self, frame):

        seq = self._get_seq()
        slot = seq % self.n_frames

        offset = 8 + slot * self.slot_size

        frame_bytes = frame.tobytes()

        struct.pack_into("I", self.buf, offset, len(frame_bytes))
        self.buf[offset+4:offset+4+len(frame_bytes)] = frame_bytes

        self._set_seq(seq + 1)

    def read_latest(self):

        seq = self._get_seq()

        if seq == 0:
            return None

        slot = (seq - 1) % self.n_frames
        offset = 8 + slot * self.slot_size

        size = struct.unpack_from("I", self.buf, offset)[0]

        data = self.buf[offset+4:offset+4+size]

        return np.frombuffer(data, dtype=np.uint8).reshape(self.shape)

    def close(self):
        self.shm.close()

    def unlink(self):
        self.shm.unlink()