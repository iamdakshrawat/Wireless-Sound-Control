import cv2
import mediapipe as mp
import math
import numpy as np

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

volume = cast(interface, POINTER(IAudioEndpointVolume))


mpDraw = mp.solutions.drawing_utils

mpHands = mp.solutions.hands
hands = mpHands.Hands()

cap = cv2.VideoCapture(0)
volBar = 400
volPer = 400

while True:
    success, img = cap.read() 
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = []
            for id, lm in enumerate(handLms.landmark):

                h , w , c = img.shape
                cx, cy =int(lm.x *w) , int(lm.y*h)
        
                lmList.append([id, cx, cy])
           

            if lmList:
                x1, y1 = lmList[4][1] , lmList[4][2]
                x2, y2 = lmList[8][1] , lmList[8][2]

                cv2.circle(img, (x1,y1), 6, (2,6,244), cv2.FILLED)
                cv2.circle(img, (x2,y2), 6, (2,6,244), cv2.FILLED)
                cv2.line(img, (x1,y1),(x2,y2),(0,0,255),4)

                length = math.hypot((x2-x1),(y2-y1))
                print(length)

                volrange = volume.GetVolumeRange()
                minvol = volrange[0]
                maxvol = volrange[1]

                vol = np.interp(length, [30 , 150 ],[minvol,maxvol])
                volBar = np.interp(length, [30 , 150 ],[400,150])
                volPer = np.interp(length, [30 , 150 ],[0,100])

                volume.SetMasterVolumeLevel(vol, None)

    cv2.rectangle(img, (30,150), (85,400),(255,0,0),3)      
    cv2.rectangle(img, (30,int(volBar)), (85,400),(255,0,0),cv2.FILLED)   
    cv2.putText(img, f'{int(volPer)} %',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)   


    cv2.imshow("Image", img)


    if cv2.waitKey(1) == 27:
        break
  
cv2.destroyAllWindows()
