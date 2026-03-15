import cv2
import numpy as np
streams = [
"udp://127.0.0.1:5000?fifo_size=500000&overrun_nonfatal=1",
"udp://127.0.0.1:5001?fifo_size=500000&overrun_nonfatal=1",
"udp://127.0.0.1:5002?fifo_size=500000&overrun_nonfatal=1",
"udp://127.0.0.1:5003?fifo_size=500000&overrun_nonfatal=1",
"udp://127.0.0.1:5004?fifo_size=500000&overrun_nonfatal=1",
"udp://127.0.0.1:5005?fifo_size=500000&overrun_nonfatal=1",
"udp://127.0.0.1:5006?fifo_size=500000&overrun_nonfatal=1",
"udp://127.0.0.1:5007?fifo_size=500000&overrun_nonfatal=1",
]

caps = [cv2.VideoCapture(s, cv2.CAP_FFMPEG) for s in streams]

for c in caps:
    c.set(cv2.CAP_PROP_BUFFERSIZE, 1)

while True:

    frames = []

    for cap in caps:
        ret, frame = cap.read()
        if not ret:
            frames.append(None)
        else:
            frames.append(frame)

    if any(f is None for f in frames):
        continue

    # Top row
    top = np.hstack((frames[0], frames[1], frames[2], frames[3]))

    # Bottom row
    bottom = np.hstack((frames[4], frames[5], frames[6], frames[7]))

    # Full frame
    full = np.vstack((top, bottom))

    cv2.imshow("Reconstructed Frame", full)

    if cv2.waitKey(1) == 27:
        break

for c in caps:
    c.release()

cv2.destroyAllWindows()