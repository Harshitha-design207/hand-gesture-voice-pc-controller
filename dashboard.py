import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import speech_recognition as sr
import pyttsx3
import pywhatkit
import webbrowser
import threading
import os
import mediapipe as mp
import pyautogui
import math
import psutil

# ---------------- SETTINGS ----------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

engine = pyttsx3.init()

pyautogui.FAILSAFE = False

# ---------------- DASHBOARD ----------------

class Dashboard:

    def __init__(self):

        self.root = ctk.CTk()

        self.root.geometry("1500x850")

        self.root.title("AI Gesture + Voice Controller")

        # CAMERA
        self.cap = cv2.VideoCapture(0)

        # HAND TRACKING
        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7
        )

        self.mp_draw = mp.solutions.drawing_utils

        # UI
        self.create_ui()

        # START CAMERA
        self.update_camera()

        # START SYSTEM MONITOR
        self.update_system()

        # START VOICE SYSTEM
        threading.Thread(
            target=self.voice_system,
            daemon=True
        ).start()

        self.root.mainloop()

    # ---------------- UI ----------------

    def create_ui(self):

        # TITLE
        title = ctk.CTkLabel(
            self.root,
            text="AI HAND GESTURE + VOICE CONTROLLER",
            font=("Arial", 32, "bold"),
            text_color="cyan"
        )

        title.pack(pady=20)

        # MAIN FRAME
        main = ctk.CTkFrame(self.root)

        main.pack(fill="both", expand=True, padx=20, pady=20)

        # LEFT CAMERA FRAME
        left = ctk.CTkFrame(main)

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.camera_label = ctk.CTkLabel(
            left,
            text=""
        )

        self.camera_label.pack(pady=20)

        # RIGHT PANEL
        right = ctk.CTkFrame(
            main,
            width=350
        )

        right.pack(
            side="right",
            fill="y",
            padx=20,
            pady=20
        )

        # STATUS TITLE
        status = ctk.CTkLabel(
            right,
            text="AI STATUS",
            font=("Arial", 28, "bold"),
            text_color="lime"
        )

        status.pack(pady=20)

        # VOICE STATUS
        self.voice_label = ctk.CTkLabel(
            right,
            text="Voice : Waiting",
            font=("Arial", 20)
        )

        self.voice_label.pack(pady=20)

        # GESTURE STATUS
        self.gesture_label = ctk.CTkLabel(
            right,
            text="Gesture : Waiting",
            font=("Arial", 20)
        )

        self.gesture_label.pack(pady=20)

        # AI STATUS
        self.ai_label = ctk.CTkLabel(
            right,
            text="AI : Ready",
            font=("Arial", 20)
        )

        self.ai_label.pack(pady=20)

        # CPU STATUS
        self.cpu_label = ctk.CTkLabel(
            right,
            text="CPU : 0%",
            font=("Arial", 18)
        )

        self.cpu_label.pack(pady=10)

        # RAM STATUS
        self.ram_label = ctk.CTkLabel(
            right,
            text="RAM : 0%",
            font=("Arial", 18)
        )

        self.ram_label.pack(pady=10)

        # BUTTONS

        google_btn = ctk.CTkButton(
            right,
            text="Open Google",
            height=50,
            command=lambda:webbrowser.open(
                "https://google.com"
            )
        )

        google_btn.pack(
            fill="x",
            padx=20,
            pady=10
        )

        youtube_btn = ctk.CTkButton(
            right,
            text="Open YouTube",
            height=50,
            command=lambda:webbrowser.open(
                "https://youtube.com"
            )
        )

        youtube_btn.pack(
            fill="x",
            padx=20,
            pady=10
        )

        chatgpt_btn = ctk.CTkButton(
            right,
            text="Open ChatGPT",
            height=50,
            command=lambda:webbrowser.open(
                "https://chat.openai.com"
            )
        )

        chatgpt_btn.pack(
            fill="x",
            padx=20,
            pady=10
        )

        settings_btn = ctk.CTkButton(
            right,
            text="Open Settings",
            height=50,
            command=lambda:os.system(
                "start ms-settings:"
            )
        )

        settings_btn.pack(
            fill="x",
            padx=20,
            pady=10
        )

        # ACCESSIBILITY
        access = ctk.CTkLabel(
            right,
            text="Accessibility Support Enabled",
            font=("Arial", 18, "bold"),
            text_color="yellow"
        )

        access.pack(pady=30)

    # ---------------- CAMERA + GESTURE ----------------

    def update_camera(self):

        success, frame = self.cap.read()

        if success:

            frame = cv2.flip(frame, 1)

            rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            results = self.hands.process(rgb)

            h, w, c = frame.shape

            if results.multi_hand_landmarks:

                for hand_landmarks in results.multi_hand_landmarks:

                    self.mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS
                    )

                    landmarks = []

                    for lm in hand_landmarks.landmark:

                        cx = int(lm.x * w)

                        cy = int(lm.y * h)

                        landmarks.append((cx, cy))

                    # CURSOR MOVE
                    index_x, index_y = landmarks[8]

                    screen_w, screen_h = pyautogui.size()

                    screen_x = screen_w / w * index_x

                    screen_y = screen_h / h * index_y

                    pyautogui.moveTo(
                        screen_x,
                        screen_y
                    )

                    self.gesture_label.configure(
                        text="Gesture : Cursor Move"
                    )

                    # CLICK
                    thumb_x, thumb_y = landmarks[4]

                    distance = math.hypot(
                        thumb_x - index_x,
                        thumb_y - index_y
                    )

                    if distance < 30:

                        pyautogui.click()

                        self.gesture_label.configure(
                            text="Gesture : Click"
                        )

                    # OPEN CHROME
                    if landmarks[8][1] < landmarks[6][1] and \
                       landmarks[12][1] < landmarks[10][1]:

                        os.system("start chrome")

                        self.gesture_label.configure(
                            text="Gesture : Open Chrome"
                        )

                    # OPEN YOUTUBE
                    fingers_up = 0

                    tip_ids = [8, 12, 16, 20]

                    for tip in tip_ids:

                        if landmarks[tip][1] < landmarks[tip - 2][1]:

                            fingers_up += 1

                    if fingers_up == 4:

                        webbrowser.open(
                            "https://youtube.com"
                        )

                        self.gesture_label.configure(
                            text="Gesture : Open YouTube"
                        )

            image = Image.fromarray(rgb)

            image = image.resize((850, 550))

            photo = ImageTk.PhotoImage(image)

            self.camera_label.configure(image=photo)

            self.camera_label.image = photo

        self.root.after(10, self.update_camera)

    # ---------------- SYSTEM STATUS ----------------

    def update_system(self):

        cpu = psutil.cpu_percent()

        ram = psutil.virtual_memory().percent

        self.cpu_label.configure(
            text=f"CPU : {cpu}%"
        )

        self.ram_label.configure(
            text=f"RAM : {ram}%"
        )

        self.root.after(1000, self.update_system)

    # ---------------- SPEAK ----------------

    def speak(self, text):

        self.ai_label.configure(
            text=f"AI : {text}"
        )

        engine.say(text)

        engine.runAndWait()

    # ---------------- LISTEN ----------------

    def listen(self):

        recognizer = sr.Recognizer()

        with sr.Microphone() as source:

            self.voice_label.configure(
                text="Voice : Listening..."
            )

            recognizer.adjust_for_ambient_noise(source)

            audio = recognizer.listen(source)

        try:

            command = recognizer.recognize_google(audio)

            command = command.lower()

            self.voice_label.configure(
                text=f"Voice : {command}"
            )

            return command

        except:

            return ""

    # ---------------- COMMAND EXECUTION ----------------

    def execute_command(self, command):

        # OPEN GOOGLE
        if "open google" in command:

            self.speak("Opening Google")

            webbrowser.open(
                "https://google.com"
            )

        # OPEN YOUTUBE
        elif "open youtube" in command:

            self.speak("Opening YouTube")

            webbrowser.open(
                "https://youtube.com"
            )

        # OPEN CHATGPT
        elif "open chatgpt" in command:

            self.speak("Opening ChatGPT")

            webbrowser.open(
                "https://chat.openai.com"
            )

        # PLAY SONG
        elif "play" in command:

            song = command.replace(
                "play",
                ""
            )

            self.speak(
                f"Playing {song}"
            )

            pywhatkit.playonyt(song)

        # SEARCH
        elif "search" in command:

            query = command.replace(
                "search",
                ""
            )

            self.speak(
                f"Searching {query}"
            )

            pywhatkit.search(query)

        # OPEN SETTINGS
        elif "open settings" in command:

            self.speak(
                "Opening Settings"
            )

            os.system(
                "start ms-settings:"
            )

        # OPEN NOTEPAD
        elif "open notepad" in command:

            self.speak(
                "Opening Notepad"
            )

            os.system(
                "start notepad"
            )

        # GENERAL SEARCH
        else:

            self.speak(
                "Searching Google"
            )

            pywhatkit.search(command)

    # ---------------- VOICE LOOP ----------------

    def voice_system(self):

        while True:

            command = self.listen()

            if command:

                self.execute_command(command)

# ---------------- RUN ----------------

Dashboard()