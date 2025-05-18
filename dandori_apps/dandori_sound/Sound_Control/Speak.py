#
# May 2025. Created by Hibiya Haraki
#
# Speak.py
#

import pyttsx3
from time import sleep
import sounddevice as sd

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