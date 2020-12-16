import cv2
import imutils
from imutils.object_detection import non_max_suppression
import numpy as np

cap = cv2.VideoCapture("LondonWalk_Trim.mp4")

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def GetContours():
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    diff = cv2.absdiff(frame1,frame2)
    gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    _ , thresh = cv2.threshold(blur,20,255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(frame1,contours, -1, (0,255,0), 2)

    return thresh

def detector(image):
    #image = imutils.resize(image, width=min(400, image.shape[1]))
    clone = image.copy()
    rects, weights = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)
    for (x, y, w, h) in rects:
       cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    result = non_max_suppression(rects, probs=None, overlapThresh=0.9)
    return result


ret, frame1 = cap.read()
ret, frame2 = cap.read()
while cap.isOpened():


    result = detector(frame1.copy())
    result1 = len(result)
    
    #diff = cv2.absdiff(frame1,frame2)
    #gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    #blur = cv2.GaussianBlur(gray,(5,5),0)
    #_ , thresh = cv2.threshold(blur,20,255, cv2.THRESH_BINARY)
    #dilated = cv2.dilate(thresh, None, iterations=3)
    #contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #cv2.drawContours(frame1,contours, -1, (0,255,0), 2)

    print (result1)
    for (xA, yA, xB, yB) in result:
        cv2.rectangle(frame1, (xA, yA), (xB, yB), (0, 255, 0), 2)
    


    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()