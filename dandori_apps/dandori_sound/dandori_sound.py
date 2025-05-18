#
# May 2025. Created by Hibiya Haraki
#
# dandori_sound.py
#

from time import sleep
from flask import render_template
from datetime import datetime, date, timedelta, time
from sqlalchemy import union_all

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

# Compare text
# from dandori_apps.dandori_sound.compare_text import compare_text

# Sound response
import sounddevice as sd
import queue
from vosk import Model, KaldiRecognizer
import pyttsx3
import json

# Compare text
from transformers import BertTokenizer, BertModel
import torch
from scipy.spatial.distance import cosine

# Voice recognition
model = Model("model-en-sm")
recognizer = KaldiRecognizer(model, 16000)
q = queue.Queue()

#Compare text setting
model_name = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# Read text with speak engine
def read_text(text):
    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', 180)
    voices = engine.getProperty('voices')
    for voice in voices:
        if "English" in voice.name:
            engine.setProperty('voice', voice.id)
            print(f"Language: {voice.name}")
            break
    
    # Speak up text
    engine.say(text)

    # Execute speak
    engine.runAndWait()
    engine.stop()
    sleep(1)

# Callback function for voice
def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

# Convert string to vector
def get_sentence_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze().numpy()

# Compare text
def compare_text(text1, text2):
    vec1 = get_sentence_embedding(text1)
    vec2 = get_sentence_embedding(text2)

    similarity = 1 - cosine(vec1, vec2)
    print("Similarity: {}".format(similarity))

    if similarity > 0.9:
        return True
    else:
        return False

# Reply today's step
def reply_today_step():
    # Get Steps
    filtered_steps_db_today = db.session.query(Step_DB) \
        .filter(Step_DB.due_date >= datetime.combine(date.today(), time()))\
        .filter(Step_DB.due_date <  datetime.combine(date.today(), time()) + timedelta(days=1))\
        .order_by(Step_DB.due_date)
    filtered_steps_db_past = db.session.query(Step_DB) \
        .filter(Step_DB.status != "DONE") \
        .filter(Step_DB.due_date < datetime.combine(date.today(), time()))\
        .order_by(Step_DB.due_date)
    to_do_steps = []
    if (filtered_steps_db_past.count() > 0):
        for step_db in filtered_steps_db_past:
            step = Step(step_db)
            to_do_steps.append(step)
    if (filtered_steps_db_today.count() > 0):
        for step_db in filtered_steps_db_today:
            step = Step(step_db)
            to_do_steps.append(step)
    
    read_text_str = "Today you have {0} tasks".format(len(to_do_steps))
    for idx, step in enumerate(to_do_steps):
        read_text_str += "\n" + "Step No.{0} is {1}. You need to finish by {2}".format(idx+1,step.name,step.due_date.due_date)
    
    return read_text_str

# Main function
def response_sound():
    print("Check database access from here {0}".format(db.session.query(Step_DB).count()))
    with sd.RawInputStream(samplerate=16000, blocksize=1000, dtype='int16',
                        channels=1, callback=callback):
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get("text", "")
                print("Voice recognition:", text)
                if (compare_text(text,"What is today's task for me?")):
                    read_text("Hello Hibiya! Thank you for asking question.")
                    read_text(reply_today_step())
                    read_text("Do you have any more questions?")

@app.route('/')
def index():
    render_template('index.html')
    response_sound()