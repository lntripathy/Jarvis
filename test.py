import pyttsx3
import time

engine = pyttsx3.init()
engine.say("Hello! If you hear this, pyttsx3 is working.")
engine.runAndWait()
time.sleep(0.2)  # Small delay for processing
engine.say("I am working again.")
engine.runAndWait()
engine.stop()

