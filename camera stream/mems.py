# from multiprocessing import shared_memory
# import numpy as np
# import time

# # Create a NumPy array with data
# data = np.array([1, 2, 3, 4, 5])
# c=0
# # Create shared memory and allocate enough space for the array's bytes
# shm = shared_memory.SharedMemory(name='MyMemory', create=True, size=data.nbytes)
# # Create a NumPy array that uses the shared memory buffer
# shared_array = np.ndarray(data.shape, dtype=data.dtype, buffer=shm.buf)
# # Copy data into the shared memory array
# try:
#     while True:
#         l = [c, 2, 3, 4, 5]
#         data = np.array(l)
#         shared_array[:] = data[:]
#         c+=1
#         time.sleep(1)
# except KeyboardInterrupt:
#     shm.close()
#     shm.unlink()



# # print(f"Process 1 wrote: {shared_array[:]}")
# # # In a real scenario, this process would now start other processes 
# # # and pass the 'MyMemory' name for them to attach to.
# # # We keep it alive here for demonstration.
# # input("Press Enter to close and unlink shared memory...")

#  # Releases the shared memory segment

import time

import dualBuff

try:
    ipc = dualBuff.DualBufferIPC(create=True)
except:
    ipc = dualBuff.DualBufferIPC()

i = 0
while True:
    if i==100:
        break
    msg = f"{i}".encode()
    ipc.write(msg)
    i += 1
    # time.sleep(0.00001)
