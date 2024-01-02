import cv2 as cv
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import HandTrackingModule as htm

cap = cv.VideoCapture(0) 
cap.set(3,1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.6, maxHands=1)
dt = htm.handDetector(detectionCon= 0.7 )

class DragRect():
    def __init__(self, posCenter, size=(200,200), colorR = (255,0,150)):
        self.posCenter = posCenter
        self.size = size
        self.colorR = colorR

    def update(self,cursor):
        cx,cy = self.posCenter
        w,h = self.size

        if cx-w//2<cursor[0]<cx+w//2 and cy-h//2<cursor[1]<cy+h//2:
            self.colorR = (0,255,0)
            self.posCenter=cursor[0], cursor[1]
        else:
            self.colorR = (255,0,150)

colorR = (255,0,150)
cx,cy,w,h  = 100,100,200,200
rectList = []
for x in range(5):
    rectList.append(DragRect([x*250+150,150]))

while True:
    isTrue, img = cap.read()
    img = cv.flip(img, 1)
    allHands, img = detector.findHands(img, flipType=False)
    

    if allHands:
        hand = allHands[0]
        lmList = hand["lmList"] 
        bbox = hand["bbox"] 
        centerPoint = hand["center"] 
        handType = hand["type"]
        
        if lmList:

            l, info, img=detector.findDistance(p1=(lmList[8][0],lmList[8][1]),p2=(lmList[12][0],lmList[12][1]),img=img)
            
            print(l)

            if l<50:
                cursor = lmList[8] 
                for rect in rectList:
                    rect.update(cursor)
                
    for rect in rectList:
        cx,cy = rect.posCenter
        w,h = rect.size
        colorR = rect.colorR
        cv.rectangle(img, (cx-w//2,cy-h//2), (cx+w//2,cy+h//2), colorR, -1)

    

    cv.imshow('Camera',img)



    if cv.waitKey(20) & 0xFF==ord('d'):
        break

cap.release()
cv.destroyAllWindows()