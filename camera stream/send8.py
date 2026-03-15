import cv2
import socket
import struct

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

addr = "127.0.0.1"

# create 8 sockets
sockets = []
ports = []

for i in range(8):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockets.append(s)
    ports.append(5000 + i)

frame_id = 0

while True:

    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape

    tile_w = w // 4
    tile_h = h // 2

    tiles = []

    # split into 4x2 grid
    for r in range(2):
        for c in range(4):

            tile = frame[
                r * tile_h:(r + 1) * tile_h,
                c * tile_w:(c + 1) * tile_w
            ]

            tiles.append(tile)

    for i, tile in enumerate(tiles):

        _, buffer = cv2.imencode(
            ".jpg",
            tile,
            [cv2.IMWRITE_JPEG_QUALITY, 50]
        )

        header = struct.pack("IB", frame_id, i)

        sockets[i].sendto(
            header + buffer.tobytes(),
            (addr, ports[i])
        )

    frame_id += 1