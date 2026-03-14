import cv2

url = "rtmp://localhost/live/test"

cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()
    if not ret:
        print("No frame")
        break

    cv2.imshow("stream", frame)

    if cv2.waitKey(1) == 27:
        break