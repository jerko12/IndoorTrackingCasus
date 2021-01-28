import tkinter as tk
import pyrebase
import datetime
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template

app = Flask(__name__)

config = {
    "apiKey": "AIzaSyCr2H0WACeTfZWxPSqE-h3UORXcR439Mts",
    "authDomain": "indoor-tracking-89bd9.firebaseapp.com",
    "databaseURL": "https://indoor-tracking-89bd9-default-rtdb.europe-west1.firebasedatabase.app",
    "storageBucket": "indoor-tracking-89bd9.appspot.com",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

retrieve_data = db.child("Rooms").child("Room1").child("13").child("40").get()

time = datetime.datetime.now()

retrieved_data_list = []
plt.figure(figsize=(20, 8))


def retrieve_data_range_time(start_hour, start_minute, end_hour, end_minute):
    while start_hour != end_hour or start_minute != end_minute + 1:
        if start_minute == 60:
            start_hour = start_hour + 1
            start_minute = 0
        retrieve_data_range = db.child("Rooms").child("Room1").child(start_hour).child(start_minute).get()
        retrieved_data_list.append(retrieve_data_range.val())
        start_minute = start_minute + 1


def update_data_list():
    for i in range(len(retrieved_data_list)):
        if retrieved_data_list[i] == -1:
            retrieved_data_list[i] = 0


def option1():
    retrieved_data_list.clear()
    input_start_hour = int(input("Geef begin uur op: "))
    static_start_hour = str(input_start_hour)
    input_start_minute = int(input("Geef begin minuut op: "))
    static_start_minute = str(input_start_minute)
    input_end_hour = int(input("Geef eind uur op: "))
    input_end_minute = int(input("Geef eind minuut op: "))
    retrieve_data_range_time(input_start_hour, input_start_minute, input_end_hour, input_end_minute)
    update_data_list()
    start_minute_control = input_start_minute - 1

    values = []
    while input_start_hour != input_end_hour or input_start_minute != input_end_minute + 1:
        if input_start_minute == 60:
            input_start_hour = input_start_hour + 1
            input_start_minute = 0

        start_minute_control = start_minute_control + 1
        values.append(start_minute_control)
        input_start_minute = input_start_minute + 1

    values[0] = static_start_hour + ':' + static_start_minute
    plt.plot(values, retrieved_data_list)
    plt.title("aantal mensen weergeveven vanaf begin punt tot eind punt")
    plt.ylabel("aantal mensen")
    plt.xlabel("minuten oplopend vanaf " + values[0] + ' -->')
    plt.savefig('static/plot3.png')
    plt.clf()
    print('gegevens succussvol opgehaald')
    choice_option()


def image_5min_ago():
    retrieved_data_list.clear()
    retrieve_data_range_time(time.hour, time.minute - 5, time.hour, time.minute)
    retrieved_data_list.reverse()
    update_data_list()
    plt.plot(retrieved_data_list)
    plt.title('aantal mensen afgelopen 5 min')
    plt.ylabel("aantal mensen")
    plt.xlabel("aantal minuten geleden")
    plt.savefig('static/plot.png')
    plt.clf()
    print('gegevens succesvol opgehaald')
    choice_option()


def image_5min_ago2():
    retrieved_data_list.clear()
    retrieve_data_range_time(time.hour, time.minute - 5, time.hour, time.minute)
    retrieved_data_list.reverse()
    plt.plot(retrieved_data_list)
    update_data_list()
    plt.title('aantal mensen afgelopen 5 min')
    plt.ylabel("aantal mensen")
    plt.xlabel("aantal minuten geleden")
    plt.savefig('static/plot.png')
    plt.clf()
    print('gegevens succesvol opgehaald')


@app.route('/')
def dashboard():
    return render_template('home.html')


def start_website():
    app.run()


def choice_option():
    print('')
    print('Type 1 om gegevens te krijgen tussen twee tijden')
    print('Type 2 om gegevens te krijgen laatste 5 min')
    print('type 3 voor dashboard')
    choice = int(input("geef keuze: "))
    if choice == 1:
        option1()
    if choice == 2:
        image_5min_ago()
    if choice == 3:
        image_5min_ago2()
        start_website()


choice_option()
