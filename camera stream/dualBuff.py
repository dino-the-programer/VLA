# import multiprocessing as mp
# import threading
# from multiprocessing import shared_memory
# import struct
# import time

# BUF_SIZE = 1024


# class DualBufferIPC:
#     def __init__(self, name="dualbuf", create=False):
#         self.bufsize = BUF_SIZE

#         if create:
#             self.shm_a = shared_memory.SharedMemory(create=True, size=BUF_SIZE, name=name+"_a")
#             self.shm_b = shared_memory.SharedMemory(create=True, size=BUF_SIZE, name=name+"_b")
#         else:
#             self.shm_a = shared_memory.SharedMemory(name=name+"_a")
#             self.shm_b = shared_memory.SharedMemory(name=name+"_b")

#         self.buffers = [self.shm_a.buf, self.shm_b.buf]

#         self.active = mp.Value("i", 0)
#         self.write_lock = mp.Lock()

#     def write(self, data: bytes):
#         with self.write_lock:
#             inactive = 1 - self.active.value
#             buf = self.buffers[inactive]

#             size = len(data)
#             struct.pack_into("I", buf, 0, size)
#             buf[4:4+size] = data

#             self.active.value = inactive

#     def read(self):
#         idx = self.active.value
#         buf = self.buffers[idx]

#         size = struct.unpack_from("I", buf, 0)[0]
#         return bytes(buf[4:4+size])

#     def close(self):
#         self.shm_a.close()
#         self.shm_b.close()

#     def unlink(self):
#         self.shm_a.unlink()
#         self.shm_b.unlink()

import multiprocessing as mp
from multiprocessing import shared_memory
import struct


class DualBufferIPC:
    def __init__(self, name="dualbuf", BUF_SIZE = 1024 ,create=False):

        if create:
            self.shm = shared_memory.SharedMemory(create=True, size=BUF_SIZE * 2 + 16, name=name)
        else:
            self.shm = shared_memory.SharedMemory(name=name)

        self.buf = self.shm.buf
        self.BUF_SIZE = BUF_SIZE

        # memory layout
        # [0:8]   seq counter
        # [8:12]  active buffer index
        # [16:]   buffers

        self.seq = mp.Value("L", 0)
        self.lock = mp.Lock()

        self.buffer_offset = 16

    def _buffer(self, idx):
        start = self.buffer_offset + idx * self.BUF_SIZE
        return self.buf[start:start + self.BUF_SIZE]

    def write(self, data: bytes):

        with self.lock:

            # mark write begin
            self.seq.value += 1

            active = struct.unpack_from("I", self.buf, 8)[0]
            inactive = 1 - active

            buf = self._buffer(inactive)

            size = len(data)
            struct.pack_into("I", buf, 0, size)
            buf[4:4+size] = data

            struct.pack_into("I", self.buf, 8, inactive)

            # mark write complete
            self.seq.value += 1

    def read(self):

        while True:

            seq1 = self.seq.value

            if seq1 % 2 == 1:
                continue

            active = struct.unpack_from("I", self.buf, 8)[0]
            buf = self._buffer(active)

            size = struct.unpack_from("I", buf, 0)[0]
            data = bytes(buf[4:4+size])

            seq2 = self.seq.value

            if seq1 == seq2:
                return data


# if __name__ == "__main__":
#     ipc = DualBufferIPC(create=True)

#     w = threading.Thread(target=writer, args=(ipc,))
#     r1 = threading.Thread(target=reader, args=(ipc,1))
#     r2 = threading.Thread(target=reader, args=(ipc,2))
#     r3 = threading.Thread(target=reader, args=(ipc,3))

#     w.start()
#     r1.start()
#     r2.start()
#     r3.start()

#     w.join()