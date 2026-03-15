import socket
import numpy as np
import cv2
import struct
import pickle

h = 720
w = 1280

socks = []
ports = [5000,5001,5002,5003]

for p in ports:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", p))
    socks.append(s)

while True:

    parts = []

    for s in socks:
        data,_ = s.recvfrom(65536)
        frame_id = struct.unpack("I", data[:4])[0]
        part = np.frombuffer(data[4:], dtype=np.uint8)
        frame = cv2.imdecode(pickle.loads(part), cv2.IMREAD_COLOR)
        parts.append(frame)
        

    f1 = parts[0].reshape(h//2, w//2, 3)
    f2 = parts[1].reshape(h//2, w//2, 3)
    f3 = parts[2].reshape(h//2, w//2, 3)
    # f4 = parts[3].reshape(h//2, w//2, 3)
    f4 = np.zeros((h//2, w//2, 3), dtype=np.uint8)
    # f4  = cv2.cvtColor(f4, cv2.COLOR_BGR2GRAY)

    top = np.hstack((f1, f2))
    bottom = np.hstack((f3, f4))

    frame = np.vstack((top, bottom))

    cv2.imshow("Reconstructed", frame)

    if cv2.waitKey(1) == 27:
        break