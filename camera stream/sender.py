import cv2
import socket
import pickle

UDP_IP = "localhost"  # receiver IP
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)
cap

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # compress frame
    encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
    
    data = pickle.dumps(buffer)

    sock.sendto(data, (UDP_IP, UDP_PORT))

cap.release()