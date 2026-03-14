# from multiprocessing import shared_memory
# import numpy as np
# import time

# # Attach to the existing shared memory segment using its name
# shm = shared_memory.SharedMemory(name='MyMemory')
# shared_array = np.ndarray((5,), dtype=np.int64, buffer=shm.buf)

# # Create a NumPy array that uses the shared memory buffer (shape and dtype must match)
# try:
#     while True:
#         shared_array = np.ndarray((5,), dtype=np.int64, buffer=shm.buf)
#         print(f"Process 2 read: {shared_array[:]}")
#         # time.sleep(1)
# except KeyboardInterrupt:
#     shm.close() # Close the shared memory connection for this process
# # The 'unlink()' call is handled by the creator process

import dualBuff

try:
    ipc = dualBuff.DualBufferIPC(create=True)
except:
    ipc = dualBuff.DualBufferIPC()

while True:
    data = ipc.read()
    if data.decode()=="99":
        break
    print(f"reader:", data)
