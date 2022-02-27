import cv2
import time
import os
import HandTrackingModule as htm
from playsound import playsound
import smtplib
import smtplib, ssl
import imghdr
from email.message import EmailMessage

wCam, hCam = 1280,960

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "fingers"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
   image = cv2.imread(f'{folderPath}/{imPath}')
   overlayList.append(image)

print(len(overlayList))
pTime = 0

detector = htm.handDetector(detectionCon = 0.75)

tipIds = [4,8,12,16,20]

while True:

   success, img = cap.read()
   img  = detector.findHands(img)
   lmList = detector.findPosition(img, draw = False)
   #print(lmList)

   if len(lmList) != 0:
      fingers = []

      # Thumb
      if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:

          fingers.append(1)
      else:
         fingers.append(0)

      # 4 Fingers
      for id in range(1, 5):
         if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
            fingers.append(1)
         else:
            fingers.append(0)

      #print(fingers)
         totalFingers = fingers.count(1)
         print(totalFingers)

         h, w, c = overlayList[totalFingers - 1].shape
         img[0:h, 0:w] = overlayList[totalFingers - 1]

         cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
         cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                     10, (255, 0, 0), 25)

         if totalFingers == 1:
             cv2.rectangle(img, (270,150), (900, 10), (0, 255, 0), cv2.FILLED)
             cv2.putText(img, 'send location', (300, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
         if 1< totalFingers == 2:
             cv2.rectangle(img, (270,150), (900, 10), (0, 255, 0), cv2.FILLED)
             cv2.putText(img, 'message/call contacts', (300, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
         if 2< totalFingers == 3:
             cv2.rectangle(img, (270,150), (900, 10), (0, 255, 0), cv2.FILLED)
             cv2.putText(img, 'sound off alarm', (300, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
             playsound('./ALARM1.wav')
         if 3< totalFingers == 4:
             cv2.rectangle(img, (270,150), (900, 10), (0, 255, 0), cv2.FILLED)
             cv2.putText(img, 'call police', (300, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
         if 4< totalFingers == 5:
             cv2.rectangle(img, (270,150), (900, 10), (0, 255, 0), cv2.FILLED)
             cv2.putText(img, 'All of the above', (300, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)


   cTime = time.time()
   fps = 1/(cTime-pTime)
   pTime = cTime

#   cv2.putText(img, f'FPS: {int(fps)}', (400,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0),3)


   cv2.imshow("Image", img)
   cv2.waitKey(1)



