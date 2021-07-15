import math
from time import sleep
import cv2
import mediapipe as mp
import numpy as nn
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()

interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


def findPosition(img, handNo=0):
  results = hands.process(img)
  lmList = []
  if results.multi_hand_landmarks:
    myHand = results.multi_hand_landmarks[handNo]



  return lmList


def moved(f,num =[]):
  try:
    if f == num:
        return True
    else:
      return False
  except:
    pass
cap = cv2.VideoCapture(0)
tipIds = [4, 8, 12, 16, 20]
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  Rook  = False
  ii = 0
  while cap.isOpened():
    lmList = []
    success, image = cap.read()
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        for id, lm in enumerate(hand_landmarks.landmark):
          # print(id, lm)
          h, w, c = image.shape
          q, w = int(lm.x * w), int(lm.y * h)
          lmList.append([id, q, w])

        if len(lmList) != 0:
          fingers = []
          #print(lmList)
          x1, y1 = lmList[4][1], lmList[4][2]
          x2, y2 = lmList[8][1], lmList[8][2]
          cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
          cv2.inRange(image, cx, cy)
          if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            fingers.append(True)
          else:
            fingers.append(False)

          for id in range(1, 5):



            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
              fingers.append(True)
            else:
              fingers.append(False)

          if moved(fingers,[True, True, False, False, True]):
            print("\r ROOK ",end="")

          if moved(fingers,[False, False, True, False, False]):
            print("\r Noooo ",end="")

          if moved(fingers,[True, True, True, False, False]):

            cv2.circle(image,(x1,y1),15,(255,0,255),cv2.FILLED)
            cv2.circle(image,(x2,y2),15,(255,0,255),cv2.FILLED)
            cv2.line(image,(x1,y1 ),(x2,y2),(255,0,255),3)
          hh = math.hypot(x2 - x1,y2-y1)
          print(hh)
          print(Rook)
          if moved(fingers,[True, True, False, False, False]):
            cv2.circle(image, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(image, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.circle(image, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            hh = math.hypot(x2 - x1, y2 - y1)
            colorVol = (255, 0, 0)
            if hh<150:
              colorVol = (127, 0, 255)
            if hh<80:
              colorVol = (0, 0, 255)



              #nn.vo
            volBar = nn.interp(hh, [50, 200], [400, 150])

            volPer = nn.interp(hh, [50, 200], [0, 100])

            smoothness = 1
            volPer = smoothness * round(volPer / smoothness)
            volume.SetMasterVolumeLevelScalar(volPer / 100, None)
            cv2.circle(image, (cx, cy), 15, colorVol, cv2.FILLED)

            volume.SetMasterVolumeLevelScalar(volPer / 100, None)



              # Drawings
            cv2.rectangle(image, (10, 150), (85, 400), colorVol, 3)
            cv2.rectangle(image, (10, int(volBar)), (85, 400), colorVol, cv2.FILLED)
            cVol = int(volume.GetMasterVolumeLevelScalar() * 100)







        mp_drawing.draw_landmarks(
          image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    cv2.imshow('Fingrs', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break



cap.release()