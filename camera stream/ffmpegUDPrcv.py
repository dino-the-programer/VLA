import cv2

cap = cv2.VideoCapture(
    "udp://127.0.0.1:5000?fifo_size=100000&overrun_nonfatal=1",
    cv2.CAP_FFMPEG
)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Frame not received")
        break

    cv2.imshow("UDP Stream", frame)

    if cv2.waitKey(1) == 27:
        break