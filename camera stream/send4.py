import cv2
import socket
import struct
import pickle

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

addr = "127.0.0.1"

frame_id = 0

while True:
    ret, frame = cap.read()
    # _, frame = cv2.imencode(".jpg", frame)
    if not ret:
        break

    h, w, _ = frame.shape
    # split frame
    f1 = frame[0:h//2, 0:w//2]
    f2 = frame[0:h//2, w//2:w]
    f3 = frame[h//2:h, 0:w//2]
    f4 = frame[h//2:h, w//2:w]
    encoded1, buffer1 = cv2.imencode('.jpg', f1, [cv2.IMWRITE_JPEG_QUALITY, 50])
    encoded2, buffer2 = cv2.imencode('.jpg', f2, [cv2.IMWRITE_JPEG_QUALITY, 50])
    encoded3, buffer3 = cv2.imencode('.jpg', f3, [cv2.IMWRITE_JPEG_QUALITY, 50])
    encoded4, buffer4 = cv2.imencode('.jpg', f4, [cv2.IMWRITE_JPEG_QUALITY, 50])

    data1 = pickle.dumps(buffer1)
    data2 = pickle.dumps(buffer2)
    data3 = pickle.dumps(buffer3)
    data4 = pickle.dumps(buffer4)

    header = struct.pack("I", frame_id)
    # print(len(header + f1.tobytes()))

    sock1.sendto(header + data1, (addr, 5000))
    sock2.sendto(header + data2, (addr, 5001))
    sock3.sendto(header + data3, (addr, 5002))
    sock4.sendto(header + data4, (addr, 5003))

    frame_id += 1