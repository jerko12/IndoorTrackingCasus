import cv2
import imutils
from imutils.object_detection import non_max_suppression
import numpy as np
import pyrebase
import datetime


#Trackers
trDict = {'csrt' : cv2.TrackerCSRT_create,
'kcf' : cv2.TrackerKCF_create,
'boosting' : cv2.TrackerBoosting_create,
'mil' : cv.TrackerMIL_create,
'tld' : cv2.TrackerTLD_create,
'medianflow' : cv2.TrackerMedianFlow_create,
'mosse' : cv2.TrackerMOSSE_create
}


roomName = "Room1"

#Firebase
firebaseConfig={
    'apiKey': "AIzaSyCr2H0WACeTfZWxPSqE-h3UORXcR439Mts",
    'authDomain': "indoor-tracking-89bd9.firebaseapp.com",
    'databaseURL': "https://indoor-tracking-89bd9-default-rtdb.europe-west1.firebasedatabase.app",
    'projectId': "indoor-tracking-89bd9",
    'storageBucket': "indoor-tracking-89bd9.appspot.com",
    'messagingSenderId': "900801920066",
    'appId': "1:900801920066':web:d8e25b256dc3739a5581db",
    'measurementId': "G-52TF0D1RCD"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

db.child("Rooms").child("Room1").child("12").child("0").set(3)

hours = 0
minutes = 0

#for hour in range(0,24):
 #   for minute in range(0,60):
  #      db.child("Rooms").child("Room1").child(str(hour)).child(str(minute)).set(-1)

def databaseCreate():
    print("CreateNewData")

def databaseRead():
    print("Read Database")
    #db.child("Rooms").child(str(roomName)).child("13").child("40").get()

def databaseUpdate(roomName,hour,minute,data):
    print("Update Database " + str(roomName) + "   " + str(hour) +":" + str(minute) +" : " + str(data))
    db.child("Rooms").child(str(roomName)).child(str(hour)).child(str(minute)).set(data)

    

#Open CV
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
    rects, weights = hog.detectMultiScale(image, winStride=(3, 3), padding=(16, 16), scale=0.25)
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
            weight = 0.01
        average = (average * weight * averageCount + currentCount) / (averageCount* weight + 1)

    return average


def Reset():
    global avarage
    global averageCount
    average = 0
    averageCount = 0


def Program():
    

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    global average 
    global averageCount
    global result
    lastTime = datetime.datetime.now()
    while cap.isOpened():

        frame1 = imutils.resize(frame1, width=min(400, frame1.shape[1]))
        frame1 = imutils.resize(frame1, width=max(800, frame1.shape[1]))
        result,weights = detector(frame1.copy())
        result1 = len(result)
        

        average = calculateAverage(average, averageCount ,result1)
        averageCount += 1
        print(result1,average,averageCount)

        currentTime = datetime.datetime.now()
        if(lastTime.minute != currentTime.minute):
            print("H: " + str(currentTime.hour) + "  M: " + str(currentTime.minute))
            databaseUpdate(roomName,currentTime.hour,currentTime.minute,int(round(average)))
            Reset()
            lastTime = currentTime

        setRectangles(frame1,result,weights)

        frame1 = imutils.resize(frame1, width=max(600, frame1.shape[1]))
        cv2.imshow("feed", frame1)
        frame1 = frame2
        ret, frame2 = cap.read()

        if cv2.waitKey(40) == 27:
            break


average = 0
averageCount = 0
global result

Program()

cv2.destroyAllWindows()
cap.release()