import cv2
import mediapipe as mp
import time
from directkeys import right_pressed, left_pressed
from directkeys import PressKey, ReleaseKey


next_slide_key = right_pressed #for next slides
previous_slide_key = left_pressed  # for the previous slides 

time.sleep(2.0)
current_key_pressed = set()
last_action = None  # check the last action thats processed
action_cooldown = 0.5  

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

tipIds = [4, 8, 12, 16, 20]

video = cv2.VideoCapture(0)
with mp_hand.Hands(min_detection_confidence=0.5,
               min_tracking_confidence=0.5) as hands:
    while True:
        keyPressed = False

        ret, image = video.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        lmList = []

        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                myHands = results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])

        fingers = []
        if len(lmList) != 0:
            # Check thumb position
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                fingers.append(1)  
            else:
                fingers.append(0)  

            # Check other fingers
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1) 
                else:
                    fingers.append(0) 

            total = fingers.count(1)

            # Check for fist closure (all fingers down)
            if total == 0 and last_action != "fist_closed":
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "NEXT SLIDE", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                PressKey(next_slide_key)
                current_key_pressed.add(next_slide_key)
                keyPressed = True
                last_action = "fist_closed"  
                time.sleep(action_cooldown) 
                ReleaseKey(next_slide_key) 
            
            elif total == 5 and last_action != "fist_open":
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "NEXT SLIDE", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                PressKey(next_slide_key)
                current_key_pressed.add(next_slide_key)
                keyPressed = True
                last_action = "fist_open" 
                time.sleep(action_cooldown)  
                ReleaseKey(next_slide_key) 

           
            elif total == 2 and fingers[1] == 1 and fingers[2] == 1 and last_action != "two_fingers":
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "PREVIOUS SLIDE", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                PressKey(previous_slide_key)
                current_key_pressed.add(previous_slide_key)
                keyPressed = True
                last_action = "two_fingers"  
                time.sleep(action_cooldown)  
                ReleaseKey(previous_slide_key)  

       
        if not keyPressed and len(current_key_pressed) != 0:
            for key in current_key_pressed:
                ReleaseKey(key)
            current_key_pressed = set()

        cv2.imshow("Frame", image)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

video.release()
cv2.destroyAllWindows()
