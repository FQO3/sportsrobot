import cv2
import PoseModule as pm
import requests
import sound
import threading
from datetime import *
import os
cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
msg = 0
form = 0
feedback = "Go Up!"
stime = datetime.now()
data=dict(sec='0')
startflag=False 

def req(dat):
    try:
        requests.post("http://192.168.4.1/AU",params=dat,timeout=0.2)
    except requests.exceptions.Timeout:
        print("Connection Timeout!!! Please check your raspi!!!")
def music():
    sound.voice.play()
musicTh=threading.Thread(target=music)
musicTh.daemon=True
#主程序
musicTh.start()
while cap.isOpened():
    if startflag==0:
        req(data)
        startflag=1
    ret, img = cap.read()
    width = cap.get(3)
    height = cap.get(4)

    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        rshoulder = detector.findAngle(img, 13, 11, 23)
        lshoulder = detector.findAngle(img, 14, 12, 24)

        if  form==0 and rshoulder > 80 and rshoulder <120 and lshoulder >80 and lshoulder<120:
            form = 1
            feedback = "Keep!"
            stime=datetime.now()

        if form==1:
            if(rshoulder < 80 or rshoulder >120 or lshoulder <80 or lshoulder>120):
                form = 0
                feedback = "Go Up!"
                data=dict(sec='0')
                req(data)
        
        if form==1:
            ntime=datetime.now()-stime
            timer=str(int(ntime.seconds/60))+" min "+str(ntime.seconds%60)+" sec "
            print(timer)
            cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, timer, (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,(255, 0, 0), 5)
            if msg != ntime.seconds:
                msg=ntime.seconds
                data=dict(sec=msg)
                req(data)
                if ntime.seconds%10==0 and ntime.seconds!=0:
                    os.system("python act/say.py")
                
        cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2,
                    (0, 255, 0), 2)
    

    cv2.imshow('Arm Up counter', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
