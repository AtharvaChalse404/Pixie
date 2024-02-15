import speech_recognition as sr
import pyttsx3
import datetime
import requests

# Define the API endpoint URL
url = 'https://api.tomorrow.io/v4/weather/forecast'

# Define the API key
api_key = 'YOUR_API_KEY_HERE'

# Initialize speech recognition
recognizer = sr.Recognizer()

# Initialize text to speech engine with the 'sapi5' driver
engine = pyttsx3.init(driverName='sapi5')
engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

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
            # Make the GET request to the Tomorrow.io Weather API
            response = requests.get(url, params={'location': '42.3478,-71.0466', 'apikey': api_key})
            if response.status_code == 200:
                weather_data = response.json()
                # Extract relevant weather information from the response
                temperature = weather_data['temperature']['value']
                weather_description = weather_data['weather']['description']
                speak(f"The weather is {weather_description} with a temperature of {temperature} degrees Celsius.")
            else:
                speak(f"Sorry, there was an error fetching the weather data. Error code {response.status_code}.")
                
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
        
    except Exception as e:
        print(e)
        speak("An error occurred. Please try again later.")

if __name__ == "__main__":
    speak("Hello! I am your virtual assistant. How can I assist you today?")
    while True:
        assistant()
