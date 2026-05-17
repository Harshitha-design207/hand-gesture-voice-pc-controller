import cv2
import threading

from hand_tracking import HandTracker
from gesture_controller import move_cursor, perform_click, open_app_by_gesture
from voice_assistant import listen, execute_voice_command

tracker = HandTracker()

cap = cv2.VideoCapture(0)

def voice_system():

    while True:

        command = listen()

        if command:

            execute_voice_command(command)

voice_thread = threading.Thread(target=voice_system)

voice_thread.daemon = True

voice_thread.start()

while True:

    success, frame = cap.read()

    frame = cv2.flip(frame, 1)

    frame, landmarks = tracker.detect_hands(frame)

    if landmarks:

        index_x = landmarks[8][1]
        index_y = landmarks[8][2]

        thumb_x = landmarks[4][1]
        thumb_y = landmarks[4][2]

        move_cursor(
            index_x,
            index_y,
            frame.shape[1],
            frame.shape[0]
        )

        perform_click(
            (index_x, index_y),
            (thumb_x, thumb_y)
        )
        open_app_by_gesture(landmarks)

    cv2.imshow("Hand Gesture + Voice PC Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()