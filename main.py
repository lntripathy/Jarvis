import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import cohere
import os
from dotenv import load_dotenv
# load .env
load_dotenv()


# initialization
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Improved recognizer settings for better accuracy
recognizer.energy_threshold = 300  # Adjust based on your environment
recognizer.pause_threshold = 0.8   # How long to wait for silence
recognizer.dynamic_energy_threshold = True
recognizer.non_speaking_duration = 0.5


# basic functionalities
def speak(text="Jarvis Initializing..."):  # default value is given
    engine.setProperty('rate', 180)  # slightly faster speaking
    engine.setProperty('volume', 1.0)  # max volume
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def listen():
    try:
        with sr.Microphone() as source:
            # recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            print(recognizer.energy_threshold)
            audio = recognizer.listen(source,timeout=5, phrase_time_limit=2)
        try:
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()         
        except Exception as e:
            speak("Sorry, I didn't understand that.")
            print(format(e))
            return ""

    except Exception as e:
        print("Error;")
        print(format(e))
        return ""

# AI process
api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(api_key)
def aiProcess(command):
    if not command:  # empty check
        return "I didn’t hear anything. Can you repeat?"
    try:
        response = co.chat(message=command)
        return response.text
    except Exception as e:
        return f"Error: {e}"


def processCommand(text):
    if any(phrase in text for phrase in ["open google", "google"]):
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif any(phrase in text for phrase in ["open youtube", "youtube"]):
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif any(phrase in text for phrase in ["your name", "who are you", "what's your name"]):
        speak("I am Jarvis, your AI assistant.")
    elif any(phrase in text for phrase in ["time", "what time"]):
        from datetime import datetime
        current_time = datetime.now().strftime("It's %I:%M %p")
        speak(current_time)
    elif any(phrase in text for phrase in ["date", "today's date", "what date"]):
        from datetime import datetime
        current_date = datetime.now().strftime("Today is %B %d, %Y")
        speak(current_date)
    elif any(phrase in text for phrase in ["news", "latest news", "headlines"]):
        speak("Getting the latest news for you")
        API_KEY = os.getenv("NEWS_API_KEY")
        url = 'http://api.mediastack.com/v1/news'
        params = {
            'access_key': API_KEY,
            'countries': 'in',        # For India
            'languages': 'en',        # English news
            'limit': 5,               # Top 5 news articles
            'sort': 'published_desc'  # Newest first
        }

        

        # Make the request
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data and data['data']:
                    speak("Here are the top news headlines")
                    for i, article in enumerate(data['data'], 1):
                        speak(f"News {i}: {article['title']}")
                        print(f"News {i}: {article['title']}")
                else:
                    speak("Sorry, I couldn't fetch the news right now")
            else:
                speak("Sorry, there was an issue getting the news")
        except Exception as e:
            speak("Sorry, I couldn't access the news service")
            print(f"News API error: {e}")
    
    else:
        # let cohere AI Handle the request...
        speak("Let me think about that")
        output = aiProcess(text)
        speak(output)

    
    


# main execution
if __name__ == "__main__":
    speak()
    while True:    
        user_input = listen()
        if "jarvis" in user_input:
            print("jarvis activated...")
            speak("Yes Sir!")
            user_input = listen()
            processCommand(user_input)
        elif any(x in user_input for x in ["bye", "exit", "shutdown", "quit"]):
            speak("Have a good day Gudu Bhaaina :)")
            break