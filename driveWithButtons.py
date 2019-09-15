from wheelMovementLogic import WheelMovementLogic
from mainboardCommunication import MainboardCommunication

import serial
import cv2
import numpy as np
ser = serial.Serial('/dev/ttyACM1')



frame = np.zeros((200,200))
cv2.imshow("frame",frame)
wheelLogic = WheelMovementLogic.WheelMovementLogic()
mainbComm = MainboardCommunication.MainboardCommunication()
while 1:
    key = cv2.waitKey(0) & 0xff
    print(key)
    if key == ord('w'):
        mainbComm.sendBytes(wheelLogic.setSpeed(90,-40))
    if key == ord("s"):
        mainbComm.sendBytes(wheelLogic.setSpeed(270,-40))
    if key == ord("a"):
        mainbComm.sendBytes(wheelLogic.setSpeed(180,-40))
    if key == ord("d"):
        mainbComm.sendBytes(wheelLogic.setSpeed(0,-40))
    if key == ord("c"):
        mainbComm.sendBytes(wheelLogic.rotateLeft(40))
    if key == ord("v"):
        mainbComm.sendBytes(wheelLogic.rotateRight(40))
    if key == ord('q'):
        mainbComm.sendBytes(wheelLogic.motorsOff())
        cv2.destroyAllWindows()
        ser.close()
        break
    print(mainbComm.waitForAnswer())
cv2.destroyAllWindows()
mainbComm.sendBytes(wheelLogic.motorsOff())
mainbComm.waitForAnswer()
ser.close()
