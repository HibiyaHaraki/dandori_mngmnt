#
# May 2025. Created by Hibiya Haraki
#
# Voice_Recognition.py
#

import queue
from vosk import Model, KaldiRecognizer

# Callback function for voice
def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

# Voice recognition
model = Model("model-en-sm")
recognizer = KaldiRecognizer(model, 16000)
q = queue.Queue()