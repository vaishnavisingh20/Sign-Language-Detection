import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math

# Setup
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")
offset = 20
imgSize = 300
folder = "Data/C"
counter = 0
labels = ["Hello", "Thankyou", "Yes"]

while True:
    success, img = cap.read()
    if not success:
        print(" Failed to read from camera.")
        continue

    imgOutput = img.copy()
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        # Fix the crop to be within image bounds
        y1 = max(0, y - offset)
        y2 = min(img.shape[0], y + h + offset)
        x1 = max(0, x - offset)
        x2 = min(img.shape[1], x + w + offset)

        imgCrop = img[y1:y2, x1:x2]

        # Check if the crop is valid before resizing
        if imgCrop.size != 0:
            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            aspectRatio = h / w

            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                try:
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    wGap = math.ceil((imgSize - wCal) / 2)
                    imgWhite[:, wGap:wCal + wGap] = imgResize
                except Exception as e:
                    print(f" Resize failed due to invalid crop size (tall image): {e}")
                    continue
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                try:
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap:hCal + hGap, :] = imgResize
                except Exception as e:
                    print(f" Resize failed due to invalid crop size (wide image): {e}")
                    continue

            # Predict only if everything above succeeded
            prediction, index = classifier.getPrediction(imgWhite, draw=False)

            # Draw output
            cv2.rectangle(imgOutput, (x1, y1 - 50), (x1 + 90, y1), (255, 0, 255), cv2.FILLED)
            cv2.putText(imgOutput, labels[index], (x1 + 5, y1 - 15), cv2.FONT_HERSHEY_COMPLEX, 1.3, (255, 255, 255), 2)
            cv2.rectangle(imgOutput, (x1, y1), (x2, y2), (255, 0, 255), 4)

            # Show windows
            cv2.imshow("ImageCrop", imgCrop)
            cv2.imshow("ImageWhite", imgWhite)
        else:
            print(" Empty crop. Skipping frame.")

    # Always show the main image
    cv2.imshow("Image", imgOutput)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
