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

        print("Say Command...")

        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source)

    try:

        command = recognizer.recognize_google(audio)

        command = command.lower()

        print("You Said:", command)

        return command

    except:

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

    # OPEN CHROME
    elif "open chrome" in command:

        speak("Opening Chrome")

        os.system("start chrome")

    # OPEN SETTINGS
    elif "open settings" in command:

        speak("Opening Settings")

        os.system("start ms-settings:")

    # OPEN PERFORMANCE / TASK MANAGER
    elif "open performance" in command or "open task manager" in command:

        speak("Opening Task Manager")

        os.system("start taskmgr")

    # OPEN CALCULATOR
    elif "open calculator" in command:

        speak("Opening Calculator")

        os.system("start calc")

    # OPEN NOTEPAD
    elif "open notepad" in command:

        speak("Opening Notepad")

        os.system("start notepad")

    # OPEN PAINT
    elif "open paint" in command:

        speak("Opening Paint")

        os.system("start mspaint")

    # PLAY SONGS ON YOUTUBE
    elif "play" in command:

        song = command.replace("play", "")

        speak(f"Playing {song}")

        pywhatkit.playonyt(song)

    # SEARCH ANYTHING
    elif "search" in command:

        query = command.replace("search", "")

        speak(f"Searching {query}")

        pywhatkit.search(query)

    # GENERAL GOOGLE SEARCH
    else:

        speak("Searching on Google")

        pywhatkit.search(command)