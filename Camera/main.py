
import cv2
import matplotlib.pyplot as plt
import numpy as np
from ultralytics import YOLOE

model = YOLOE("yoloe-11s-seg.pt")

names = ["red cube", "blue cube"]
# names2 = ["specs"]
model.set_classes(names,model.get_text_pe(names))


def unwarp(img, src, dst, testing):
    h, w = img.shape[:2]
    # use cv2.getPerspectiveTransform() to get M, the transform matrix, and Minv, the inverse
    M = cv2.getPerspectiveTransform(src, dst)
    # use cv2.warpPerspective() to warp your image to a top-down view
    warped = cv2.warpPerspective(img, M, (int(dst[2,0]),int(dst[2,1])), flags=cv2.INTER_LINEAR)
    # print(int(dst[2,0]),int(dst[2,1]))
    # exit()
    if testing:
        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
        f.subplots_adjust(hspace=.2, wspace=.05)
        ax1.imshow(img)
        x = [src[0][0], src[2][0], src[3][0], src[1][0], src[0][0]]
        y = [src[0][1], src[2][1], src[3][1], src[1][1], src[0][1]]
        ax1.plot(x, y, color='red', alpha=0.4, linewidth=3, solid_capstyle='round', zorder=2)
        ax1.set_ylim([h, 0])
        ax1.set_xlim([0, w])
        ax1.set_title('Original Image', fontsize=30)
        ax2.imshow(cv2.flip(warped, 1))
        ax2.set_title('Unwarped Image', fontsize=30)
        plt.show()
    else:
        return warped, M
im = cv2.imread("so.JPG")
w, h = im.shape[0], im.shape[1]

# src = np.float32([(336,55),
#                   (2133, 471),
#                   (315, 1821),
#                   (2268,  1586)])

src = np.float32([(81,90),
                  (560, 40),
                  (23, 392),
                  (622,  457)])

dst = np.float32([(1000, 0),(0, 0),(1000, 500),(0, 500)])

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

# ret, frame = cap.read()
# cv2.imwrite("scene.png",frame)

# exit()

while(True):
    ret, frame = cap.read()
    if not ret:
        break
    wrapped,_ = unwarp(frame, src, dst, False)
    results = model.predict(cv2.flip(wrapped, 1),conf=0.1,verbose=False)
    annotated_frame = results[0].plot(boxes=True, masks=False)

    cv2.imshow("so", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.waitKey(0)
cv2.destroyAllWindows()

