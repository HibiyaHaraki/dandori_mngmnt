#
# May 2025. Created by Hibiya Haraki
#
# dandori_sound.py
#

import json
from flask import render_template
from datetime import datetime, date, timedelta, time

from ..db  import db
from dandori_apps.dandori_sound import app

from ..models.Task_DB     import Task_DB
from ..models.Step_DB     import Step_DB
from ..models.Comment_DB  import Comment_DB

# Required scripts
from ..script.Task     import *
from ..script.Step     import *
from ..script.Comment  import *
from ..script.Due_date import *
from ..script.Status   import *

# Sound Control
from .Sound_Control import *
import sounddevice as sd

# Function
from .functions import *

USER_NAME = "Hibiya"

SOUND_RECOGNITION_FLAG = True

# Main function
def response_sound():
    print("Check database access from here {0}".format(db.session.query(Step_DB).count()))
    with sd.RawInputStream(samplerate=16000, blocksize=1000, dtype='int16',
                        channels=1, callback=callback):
        while SOUND_RECOGNITION_FLAG:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get("text", "")
                print("Voice recognition:", text)

                # Response
                read_text("Hello " + USER_NAME + ". Thank you for asking")
                if (Check_Similrity_Today_Step(text)):
                    Response_Today_Step()
                if (Check_Similrity_Today_Task(text)):
                    Response_Today_Task()
                read_text("Do you have any other questions?")

def start_recognition():
    SOUND_RECOGNITION_FLAG = True
    response_sound()

def stop_recognition():
    SOUND_RECOGNITION_FLAG = False

@app.route('/')
def index():
    return render_template('index.html')