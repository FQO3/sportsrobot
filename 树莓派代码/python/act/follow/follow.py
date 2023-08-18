import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm
import requests
cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
direction = 0
form = 0
feedback = "Fix Form"
sr=-1
sl=-1
er=-1
el=-1
def req(dat):
    try:
        response=requests.post(url=dat,timeout=0.1)
    except requests.exceptions.Timeout:
        print("Connection Timeout!!! Please check your raspi!!!")
while cap.isOpened():
    ret, img = cap.read()  # 640 x 480
    # Determine dimensions of video - Help with creation of box in Line 43
    width = cap.get(3)  # float `width`
    height = cap.get(4)  # float `height`
    # print(width, height)

    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        shoulder_r = int(detector.findAngle(img, 14, 12, 24))
        shoulder_l = int(detector.findAngle(img, 13, 11, 23))
        elbow_r = int(detector.findAngle(img, 12, 14, 16))
        elbow_l = int(detector.findAngle(img, 11, 13, 15))
        
        if sr<shoulder_r-7 or sr>shoulder_r+7:
            sr=shoulder_r-180
            if sr>=-90 and sr<0:
                sr=0
            elif -180<sr and sr<-90:
                sr=180
            req('http://192.168.4.2/follow?sr={}'.format(int(sr)))
        if sl<shoulder_l-7 or sl>shoulder_l+7:
            sl=shoulder_l
            if sl>180 and sl<=270:
                sl=180
            elif sl<360 and sl>270:
                sl=0
            req('http://192.168.4.2/follow?sl={}'.format(int(sl)))
        if er<elbow_r-7 or er>elbow_r+7:
            er=270-elbow_r
            if er>180:
                er=180
            elif er<0:
                er=0
            req('http://192.168.4.2/follow?er={}'.format(int(er)))
        if el<elbow_l-7 or el>elbow_l+7:
            el=270-elbow_l
            if el>180:
                el=180
            elif el<0:
                el=0
            req('http://192.168.4.2/follow?el={}'.format(int(el)))
        # print(lmList[16][2],lmList[14][2],el,er)
    cv2.imshow('Action Follow', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
