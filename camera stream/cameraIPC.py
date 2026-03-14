import cv2
import ringBuff

def camera_process():

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("Camera failed to open")
        return
    try:
        rb = ringBuff.VideoRingBuffer(
            name="video_buffer",
            shape=(720, 1280, 3),
            n_frames=16,
            create=True
        )
    except:
        rb = ringBuff.VideoRingBuffer(
            name="video_buffer",
            shape=(720, 1280, 3),
            n_frames=16,
            create=False
        )

    print("Camera started")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Frame capture failed")
            continue

        rb.write(frame)

        # Optional preview to confirm camera works
        # cv2.imshow("camera preview", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()

camera_process()