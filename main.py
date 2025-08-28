import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import cohere
from dotenv import load_dotenv

# initialization
recognizer = sr.Recognizer()
engine = pyttsx3.init()


# basic functionalities
def speak(text="Jarvis Initializing..."):  # default value is given
    engine.setProperty('rate', 180)  # slightly faster speaking
    engine.setProperty('volume', 1.0)  # max volume
    engine.say(text)
    engine.runAndWait()

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
    if "open google" in text:
        webbrowser.open("https://www.google.com")
    elif "open youtube" in text:
        webbrowser.open("https://www.youtube.com")
    elif "your name" in text:
        speak("I am Jarvis.")
    elif "time" in text:
        from datetime import datetime
        speak(datetime.now().strftime("It's %I:%M %p"))
    elif "date" in text:
        from datetime import datetime
        speak(datetime.now().strftime("Today is %B %d, %Y"))
    elif "news" in text: 
        API_KEY = '0e92aa299d6e3e055032a8ac71a685ba'
        url = 'http://api.mediastack.com/v1/news'
        params = {
            'access_key': API_KEY,
            'countries': 'in',        # For India
            'languages': 'en',        # English news
            'limit': 5,               # Top 5 news articles
            'sort': 'published_desc'  # Newest first
        }

        # Make the request
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()

            for article in data['data']:
                speak(f"from {article['source']}    ")
                speak(f"{article['title']}") 
    else:
        # let cohere AI Handle the request...
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