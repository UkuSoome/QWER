from wheelMovementLogic import WheelMovementLogic


import cv2
import numpy as np

from gameLogic import GameLogic
from imageProccessing import ImageProcessing
from mainboardCommunication import MainboardCommunication
import threading
import time






#frame2 = np.zeros((200,200))
#cv2.imshow("frame2",frame2)
wheelLogic = WheelMovementLogic.WheelMovementLogic()

mainComm = MainboardCommunication.MainboardCommunication()


imageHandler = ImageProcessing.ImageProccessing(mainComm)



imageThread = threading.Thread(target=imageHandler.run)


imageThread.start()
time.sleep(2)
#gameHandler = GameLogic.GameLogic(imageHandler, mainComm,wheelLogic)
#gameThread = threading.Thread(target=gameHandler.run)
#gameThread.start()
while 1:
    key = imageHandler.key
    if key == ord('w'):
        print(key)
        mainComm.sendBytes(wheelLogic.setSpeed(90,-100))
        #mainComm.waitForAnswer()
    if key == ord("s"):
        mainComm.sendBytes(wheelLogic.setSpeed(270,-100))
        #mainComm.waitForAnswer()
    if key == ord("a"):
        mainComm.sendBytes(wheelLogic.setSpeed(180,-100))
        #mainComm.waitForAnswer()
    if key == ord("d"):
        mainComm.sendBytes(wheelLogic.setSpeed(0,-100))
        #mainComm.waitForAnswer()
    if key == ord("c"):
        mainComm.sendBytes(wheelLogic.rotateLeft(40))
        #mainComm.waitForAnswer()
    if key == ord("v"):
        mainComm.sendBytes(wheelLogic.rotateRight(40))
        #mainComm.waitForAnswer()
    #if key == ord('b'):
    #    gameHandler.rotateSpeed = 0
   # if key == ord('n'):
    #    gameHandler.rotateSpeed = 20
    #if key == ord('k'):
    #    mainComm.ser.write('d:1000\r\n'.encode("utf-8"))
    #if key == ord('l'):
    #    mainComm.ser.write('d:1200\r\n'.encode("utf-8"))

    if key == ord('q'):
        mainComm.sendBytes(wheelLogic.motorsOff())
        mainComm.waitForAnswer()
        cv2.destroyAllWindows()
        break
    print(mainComm.waitForAnswer())

cv2.destroyAllWindows()
mainComm.sendBytes(wheelLogic.motorsOff())
mainComm.waitForAnswer()

