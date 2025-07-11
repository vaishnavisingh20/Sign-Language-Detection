import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time
import os

# Setup
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
offset = 20
imgSize = 800
folder = "Data/Hello"
counter = 0

# Make folder if it doesn't exist
if not os.path.exists(folder):
    os.makedirs(folder)

while True:
    success, img = cap.read()
    if not success:
        print("Failed to read from camera.")
        break

    hands, img = detector.findHands(img)
    if hands:ss
        hand = hands[0]
        x, y, w, h = hand['bbox']

        # Safe crop bounds
        x1 = max(x - offset, 0)
        y1 = max(y - offset, 0)
        x2 = min(x + w + offset, img.shape[1])
        y2 = min(y + h + offset, img.shape[0])

        imgCrop = img[y1:y2, x1:x2]

        if imgCrop.size != 0:
            aspectRatio = h / w
            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255

            try:
                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    wGap = math.ceil((imgSize - wCal) / 2)
                    print(f"[INFO] Resize: imgResize shape: {imgResize.shape}, wGap: {wGap}")
                    imgWhite[:, wGap:wGap + wCal] = imgResize
                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    hGap = math.ceil((imgSize - hCal) / 2)
                    print(f"[INFO] Resize: imgResize shape: {imgResize.shape}, hGap: {hGap}")
                    imgWhite[hGap:hGap + hCal, :] = imgResize

                cv2.imshow("ImageCrop", imgCrop)
                cv2.imshow("ImageWhite", imgWhite)

            except Exception as e:
                print(f"[ERROR] During resizing or assignment: {e}")
        else:
            print("[WARNING] imgCrop is empty, skipping.")

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord("s"):
        counter += 1
        save_path = f'{folder}/Image_{time.time()}.jpg'
        cv2.imwrite(save_path, imgWhite)
        print(f"Saved image {counter}: {save_path}")

    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
