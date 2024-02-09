import speech_recognition as sr
import pyttsx3
import datetime
import pyowm

# Initialize speech recognition
recognizer = sr.Recognizer()

# Initialize text to speech engine with the 'nsss' driver
engine = pyttsx3.init(driverName='sapi5')
engine.setProperty('rate', 150)

# Get all available voices
voices = engine.getProperty('voices')

# Select a female voice
for voice in voices:
    if "female" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

# Initialize OpenWeatherMap API
owm = pyowm.OWM('c1bd515a0989b3f62208ef09c0ddb61d') 

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_weather(city):
    observation = owm.weather_at_place(city)
    w = observation.get_weather()
    temperature = w.get_temperature('celsius')['temp']
    status = w.get_detailed_status()
    return f"The weather in {city} is {status} with a temperature of {temperature} degrees Celsius."

def get_time():
    now = datetime.datetime.now()
    return f"The current time is {now.strftime('%I:%M %p')}"

def assistant():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio).lower()
        print("User:", query)

        if 'weather' in query:
            speak("Please tell me the city name.")
            city_name = recognizer.listen(source)
            city = recognizer.recognize_google(city_name)
            weather_info = get_weather(city)
            speak(weather_info)
        elif 'time' in query:
            current_time = get_time()
            speak(current_time)
        elif 'exit' in query:
            speak("Goodbye!")
            exit()
        else:
            speak("Sorry, I couldn't understand the command.")

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't understand the command.")

if __name__ == "__main__":
    speak("Hello! I am Pixie. How can I assist you today?")
    while True:
        assistant()
