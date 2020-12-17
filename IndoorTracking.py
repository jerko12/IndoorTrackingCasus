import cv2
import imutils
from imutils.object_detection import non_max_suppression
import numpy as np

cap = cv2.VideoCapture("walking.avi")

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

global averageCount
global average

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
    rects, weights = hog.detectMultiScale(image, winStride=(1, 1), padding=(8, 8), scale=0.25)
    #setRectangles(image, rects)
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    result = non_max_suppression(rects, probs=None, overlapThresh=1)
    return result,weights

def setRectangles(image, rects, weights):
    index = 0
    for (xA, yA, xB, yB) in result:
        cv2.rectangle(image, (xA, yA), (xB, yB), (0, (50 * weights[index][0]) + 100, 200 / weights[index][0]), 1)
        index += 1

def calculateAverage(average,averageCount,currentCount):
    if averageCount < 0:
        average = currentCount
    else:
        weight = 1
        if(currentCount > average):
            weight = 0.3
        average = (average * weight * averageCount + currentCount) / (averageCount* weight + 1)

    return average

ret, frame1 = cap.read()
ret, frame2 = cap.read()

average = 0
averageCount = 0
while cap.isOpened():

    #frame1 = imutils.resize(frame1, width=min(800, frame1.shape[1]))
    result,weights = detector(frame1.copy())
    result1 = len(result)
    
    #diff = cv2.absdiff(frame1,frame2)
    #gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    #blur = cv2.GaussianBlur(gray,(5,5),0)
    #_ , thresh = cv2.threshold(blur,20,255, cv2.THRESH_BINARY)
    #dilated = cv2.dilate(thresh, None, iterations=3)
    #contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #cv2.drawContours(frame1,contours, -1, (0,255,0), 2)

    #print (result1 , weights)
    average = calculateAverage(average, averageCount ,result1)
    averageCount += 1
    print(result1,average,averageCount)

    setRectangles(frame1,result,weights)
    
    

    #frame1 = imutils.resize(frame1, width=max(600, frame1.shape[1]))
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()