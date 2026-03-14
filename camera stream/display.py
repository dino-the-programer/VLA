import cv2
import ringBuff

def reader_process():

    rb = ringBuff.VideoRingBuffer(
        name="video_buffer",
        shape=(720, 1280, 3),
        n_frames=16,
        create=False
    )

    while True:
        frame = rb.read_latest()

        cv2.imshow("reader", frame)

        if cv2.waitKey(1) == 27:
            break
reader_process()