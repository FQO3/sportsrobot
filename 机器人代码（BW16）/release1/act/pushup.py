import cv2
import numpy as np
import PoseModule as pm
import requests
from datetime import *
import sound
import threading
import os
cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
direction = 0
form = 0
feedback = "Fix Form"
last = datetime.now()
flag = False
startflag=False
def music():
    sound.voice.play()
musicTh=threading.Thread(target=music)
musicTh.daemon=True
musicTh.start()

while cap.isOpened():
    if startflag==False:
        try:
            response=requests.post(url="http://192.168.4.1/pushup.html?ready=1",timeout=0.2)
        except requests.exceptions.Timeout:
            print("Connection Timeout!!! Please check your raspi!!!")
        startflag=True
    ret, img = cap.read()  # 640 x 480
    # Determine dimensions of video - Help with creation of box in Line 43
    width = cap.get(3)  # float `width`
    height = cap.get(4)  # float `height`
    # print(width, height)

    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        elbow = detector.findAngle(img, 11, 13, 15)
        shoulder = detector.findAngle(img, 13, 11, 23)
        hip = detector.findAngle(img, 11, 23, 25)

        # Percentage of success of pushup
        per = np.interp(elbow, (90, 160), (0, 100))

        # Bar to show Pushup progress
        bar = np.interp(elbow, (90, 160), (380, 50))

        # Check to ensure right form before starting the program
        if elbow > 160 and shoulder > 40 and hip > 160:
            form = 1

        # Check for full range of motion for the pushup
        if form == 1:
            if per == 0:
                if elbow <= 90 and hip > 160:
                    feedback = "Go Up!"
                    if direction == 0:
                        count += 0.5
                        direction = 1
                        try:
                            response=requests.post(url="http://192.168.4.1/PU",timeout=0.2)
                        except requests.exceptions.Timeout:
                            print("Connection Timeout!!! Please check your raspi!!!")
                        flag=True
                        last=datetime.now()
                else:
                    feedback = "Fix Form"

            if per == 100:
                if elbow > 160 and shoulder > 30 and hip > 160:
                    feedback = "Go Down!"
                    if direction == 1:
                        count += 0.5
                        direction = 0
                else:
                    feedback = "Fix Form"
                    # form = 0
        print(count)
        if flag and (datetime.now()-last).seconds>=5:
            os.system("python act/say.py")
            flag=False
        if form == 1:
            cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
            cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 0, 0), 2)

        # Pushup counter
        cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)

        # Feedback
        cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2,
                    (0, 255, 0), 2)
    else:
        flag=False
    cv2.imshow('Pushup counter', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
