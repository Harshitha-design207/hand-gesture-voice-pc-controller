import cv2
import mediapipe as mp
import pyautogui
import math
import os

# ---------------- HAND SETUP ----------------

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

screen_w, screen_h = pyautogui.size()

# ---------------- MAIN LOOP ----------------

while True:

    success, frame = cap.read()

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    h, w, c = frame.shape

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            landmarks = []

            for lm in hand_landmarks.landmark:

                cx = int(lm.x * w)

                cy = int(lm.y * h)

                landmarks.append((cx, cy))

            # ---------------- CURSOR MOVE ----------------

            index_x, index_y = landmarks[8]

            screen_x = screen_w / w * index_x

            screen_y = screen_h / h * index_y

            pyautogui.moveTo(screen_x, screen_y)

            # ---------------- CLICK ----------------

            thumb_x, thumb_y = landmarks[4]

            distance = math.hypot(
                thumb_x - index_x,
                thumb_y - index_y
            )

            if distance < 30:

                pyautogui.click()

                cv2.putText(
                    frame,
                    "CLICK",
                    (20,50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    3
                )

            # ---------------- OPEN CHROME ----------------

            if landmarks[8][1] < landmarks[6][1] and \
               landmarks[12][1] < landmarks[10][1]:

                os.system("start chrome")

                cv2.putText(
                    frame,
                    "OPEN CHROME",
                    (20,100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255,0,0),
                    3
                )

            # ---------------- OPEN YOUTUBE ----------------

            fingers_up = 0

            tip_ids = [8, 12, 16, 20]

            for tip in tip_ids:

                if landmarks[tip][1] < landmarks[tip - 2][1]:

                    fingers_up += 1

            if fingers_up == 4:

                os.system("start https://youtube.com")

                cv2.putText(
                    frame,
                    "OPEN YOUTUBE",
                    (20,150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,255),
                    3
                )

    cv2.imshow("Gesture Controller", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()

cv2.destroyAllWindows()