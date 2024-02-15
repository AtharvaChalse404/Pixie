import speech_recognition as sr
import pyttsx3
import datetime
from pyowm import OWM

recognizer = sr.Recognizer()
engine = pyttsx3.init(driverName='sapi5')
engine.setProperty('rate', 150)

owm = OWM('c1bd515a0989b3f62208ef09c0ddb61d')
weather_manager = owm.weather_manager()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_weather(city):
    observation = weather_manager.weather_at_place(city)
    w = observation.weather
    temperature = w.temperature('celsius')['temp']
    status = w.detailed_status
    return f"The weather in {city} is {status} with a temperature of {temperature} degrees Celsius."

def get_time():
    now = datetime.datetime.now()
    return f"The current time is {now.strftime('%I:%M %p')}"

def assistant():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)

        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-IN').lower()
        print("User:", query)

        if 'weather' in query:
            city_name = None
            for word in query.split():
                if word.isalpha():
                    city_name = word
                    break

            if city_name:
                print("User's City:", city_name)
                weather_info = get_weather(city_name)
                speak(weather_info)
            else:
                speak("Please specify the city name along with the question.")

        elif 'time' in query:
            current_time = get_time()
            speak(current_time)
        elif 'exit' in query:
            speak("Goodbye!")
            exit()
        else:
            speak("Sorry, I couldn't understand the command in .")

    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand the command in . Please try again.")
    except sr.RequestError:
        speak("Sorry, I'm unable to access the speech recognition service at the moment. Please try again later.")
    except Exception as e:
        print(e)
        speak("An error occurred. Please try again later.")

if __name__ == "__main__":
    speak("Hello! I am Pixie. How can I assist you today?")
    while True:
        assistant()
