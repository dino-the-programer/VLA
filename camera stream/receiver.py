import cv2
import socket
import pickle
import numpy as np

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    packet, _ = sock.recvfrom(65536)

    data = pickle.loads(packet)
    frame = cv2.imdecode(data, cv2.IMREAD_COLOR)

    cv2.imshow("Strea1", frame)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()