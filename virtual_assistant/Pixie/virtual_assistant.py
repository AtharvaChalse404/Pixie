import speech_recognition as sr
import pyttsx3
import datetime
import pyowm

# Initialize speech recognition
recognizer = sr.Recognizer()

# Initialize text to speech engine with the 'sapi5' driver
engine = pyttsx3.init(driverName='sapi5')
engine.setProperty('rate', 150)

# Get available voices and select a female voice
voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

# Initialize OpenWeatherMap API with default API key
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
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)  # Set timeout to 5 seconds

        print("Recognizing...")
        query = recognizer.recognize_google(audio).lower()
        print("User:", query)

        if 'weather' in query:
            speak("Please tell me the city name.")
            with sr.Microphone() as city_source:
                city_name_audio = recognizer.listen(city_source, timeout=5)  # Set timeout to 5 seconds
            city_name = recognizer.recognize_google(city_name_audio).lower()
            print("User's City:", city_name)
            weather_info = get_weather(city_name)
            speak(weather_info)
        elif 'time' in query:
            current_time = get_time()
            speak(current_time)
        elif 'exit' in query:
            speak("Goodbye!")
            exit()
        else:
            speak("Sorry, I couldn't understand the command.")

    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand the command. Please try again.")
    except sr.RequestError:
        speak("Sorry, I'm unable to access the speech recognition service at the moment. Please try again later.")

if __name__ == "__main__":
    speak("Hello! I am Pixie. How can I assist you today?")
    while True:
        assistant()
