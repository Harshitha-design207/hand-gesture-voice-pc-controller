import speech_recognition as sr
import pyttsx3
import webbrowser
import pywhatkit
import os

engine = pyttsx3.init()

def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)

        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)

            command = command.lower()

            print("You said:", command)

            return command

        except Exception as e:
            print("Voice Error:", e)
            return ""

def execute_voice_command(command):

    # OPEN GOOGLE
    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    # OPEN YOUTUBE
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    # OPEN CHATGPT
    elif "open chatgpt" in command:
        speak("Opening ChatGPT")
        webbrowser.open("https://chat.openai.com")

    # OPEN SETTINGS
    elif "open settings" in command:
        speak("Opening Settings")
        os.system("start ms-settings:")

    # OPEN CHROME
    elif "open chrome" in command:
        speak("Opening Chrome")
        os.system("start chrome")

    # PLAY SONG
    elif "play" in command:
        song = command.replace("play", "")
        speak(f"Playing {song}")
        pywhatkit.playonyt(song)

    # GOOGLE SEARCH
    elif "search" in command:
        search_query = command.replace("search", "")
        speak(f"Searching {search_query}")

        webbrowser.open(
            f"https://www.google.com/search?q={search_query}"
        )

    # WHAT IS / WHO IS
    elif "what is" in command or "who is" in command:
        speak("Searching Google")
        webbrowser.open(
            f"https://www.google.com/search?q={command}"
        )

    else:
        speak("Command not recognized")

