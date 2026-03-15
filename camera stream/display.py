import cv2
import ringBuff

def reader_process():

    rb = ringBuff.VideoRingBuffer(
        name="video_buffer",
        shape=(480, 640, 3),
        n_frames=16,
        create=False
    )

    while True:
        frame = rb.read_latest()
        try:
            cv2.imshow("reader", frame)
        except:
            continue

        if cv2.waitKey(1) == 27:
            break
reader_process()