import cv2
import ringBuff
import socket
import pickle

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def camera_process():

    # cap = cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    # if not cap.isOpened():
    #     print("Camera failed to open")
    #     return
    try:
        rb = ringBuff.VideoRingBuffer(
            name="video_buffer",
            shape=(480, 640, 3),
            n_frames=16,
            create=True
        )
    except:
        rb = ringBuff.VideoRingBuffer(
            name="video_buffer",
            shape=(480, 640, 3),
            n_frames=16,
            create=False
        )

    print("Camera started")

    while True:
        packet, _ = sock.recvfrom(65536)
        data = pickle.loads(packet)
        frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
        # ret, frame = cap.read()

        # if not ret:
        #     print("Frame capture failed")
        #     continue

        rb.write(frame)

        # Optional preview to confirm camera works
        # cv2.imshow("camera preview", frame)

        if cv2.waitKey(1) == 27:
            break

    # cap.release()

camera_process()