import cv2
import numpy as np

cap = cv2.VideoCapture("LondonWalk.mp4")

def FindDifferenceGrayscale():
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    diff = cv2.absdiff(frame1,frame2)
    gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    return gray

while cap.isOpened():
    ret, frame = cap.read()
    gray = FindDifferenceGrayscale()
    cv2.imshow("inter", frame)

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()