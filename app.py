from flask import Flask,render_template,url_for,request,redirect, make_response
import random
import json
from time import time
from random import random
import pyrebase
import datetime
from flask import Flask, render_template, make_response

# Front End

app = Flask(__name__)
config = {
    "apiKey": "AIzaSyCr2H0WACeTfZWxPSqE-h3UORXcR439Mts",
    "authDomain": "indoor-tracking-89bd9.firebaseapp.com",
    "databaseURL": "https://indoor-tracking-89bd9-default-rtdb.europe-west1.firebasedatabase.app",
    "storageBucket": "indoor-tracking-89bd9.appspot.com",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

peopleCountData = []

currentLength = 15
currentInterval = 2

retrieved_data_list = []

def GetTimeAfterIndex(hour,minute,index):
    for i in range(0,index):
        if(minute <= 0):
            minute = 59
            if(hour > 0):
                hour -= 1
            else:
                hour = 23
        else:
            minute -=1
    return hour,minute
    
def retreive_data(currentHour,currentMinute):
    return db.child("Rooms").child("Room1").child(str(currentHour)).child(str(currentMinute)).get().val()


@app.route('/', methods=["GET", "POST"])
def main():
    if request.method =="POST":
        global currentInterval
        global currentLength

        print(request.form["lengthRangeInput"],request.form["intervalRangeInput"])
        currentLength = int(request.form["lengthRangeInput"])
        currentInterval = int(request.form["intervalRangeInput"])
        
    
    return render_template('index.html')


@app.route('/peoplecount', methods=["GET", "POST"])
def peoplecount():
    global currentInterval
    global currentLength

    print(currentInterval,currentLength)
    currentTime = datetime.datetime.now()
    currentHour = currentTime.hour
    currentMinute = currentTime.minute

    peoplecount = []
    timestamp = []

    for i in range(0,currentLength):
        hour,minute = GetTimeAfterIndex(currentHour,currentMinute,i * currentInterval)
        timestamp.insert(0,str(hour)+":"+str("{:02d}".format(minute)))
        peoplecount.insert(0,retreive_data(hour,minute))

    data = {
        "peoplecount":peoplecount,
        "timestamp":timestamp
    }
    return data


if __name__ == "__main__":
    app.run(debug=True)