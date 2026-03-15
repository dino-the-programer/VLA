import cv2
import socket
import struct
import numpy as np
import threading

addr = "127.0.0.1"
ports = [5000,5001,5002,5003,5004,5005,5006,5007]

# store latest tiles
tiles = [None]*8
frame_ids = [None]*8

def receiver(tile_id, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((addr, port))

    while True:

        data, _ = sock.recvfrom(65535)

        frame_id, tid = struct.unpack("IB", data[:5])

        jpeg = data[5:]

        img = cv2.imdecode(
            np.frombuffer(jpeg, dtype=np.uint8),
            cv2.IMREAD_COLOR
        )

        tiles[tid] = img
        frame_ids[tid] = frame_id


# start 8 receiver threads
for i,p in enumerate(ports):
    threading.Thread(
        target=receiver,
        args=(i,p),
        daemon=True
    ).start()


while True:

    if all(t is not None for t in tiles):

        h, w, _ = tiles[0].shape

        frame = np.zeros((h*2, w*4, 3), dtype=np.uint8)

        # tiles[0] = np.zeros((tiles[0].size[], w//2, 3), dtype=np.uint8)
        # tiles[2] = cv2.cvtColor(tiles[2], cv2.COLOR_BGR2GRAY)
        # tiles[2] = cv2.cvtColor(tiles[2], cv2.COLOR_GRAY2BGR)

        # reconstruct frame
        frame[0:h,0:w] = tiles[0]
        frame[0:h,w:2*w] = tiles[1]
        frame[0:h,2*w:3*w] = tiles[2]
        frame[0:h,3*w:4*w] = tiles[3]

        frame[h:2*h,0:w] = tiles[4]
        frame[h:2*h,w:2*w] = tiles[5]
        frame[h:2*h,2*w:3*w] = tiles[6]
        frame[h:2*h,3*w:4*w] = tiles[7]

        cv2.imshow("video", frame)

        if cv2.waitKey(1) == 27:
            break