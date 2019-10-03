from wheelMovementLogic import WheelMovementLogic
from imageProccessing import ImageProcessing
from mainboardCommunication import MainboardCommunication
import threading
import time


wheelLogic = WheelMovementLogic.WheelMovementLogic()

mainComm = MainboardCommunication.MainboardCommunication('/dev/ttyACM0')


imageHandler = ImageProcessing.ImageProccessing()



imageThread = threading.Thread(target=imageHandler.run)


imageThread.start()
time.sleep(2)
mainComm.sendBytes('d:125')
while 1:
    key = imageHandler.key
    if key == ord('w'):
        mainComm.sendBytes(wheelLogic.setSpeed(90,-50))
        mainComm.waitForAnswer()
    if key == ord("s"):
        mainComm.sendBytes(wheelLogic.setSpeed(270,-50))
        mainComm.waitForAnswer()
    if key == ord("a"):
        mainComm.sendBytes(wheelLogic.setSpeed(180,-50))
        mainComm.waitForAnswer()
    if key == ord("d"):
        mainComm.sendBytes(wheelLogic.setSpeed(0,-50))
        mainComm.waitForAnswer()
    if key == ord("c"):
        mainComm.sendBytes(wheelLogic.rotateLeft(20))
        mainComm.waitForAnswer()
    if key == ord("v"):
        mainComm.sendBytes(wheelLogic.rotateRight(20))
        mainComm.waitForAnswer()
    if key == ord('k'):
        mainComm.sendBytes(wheelLogic.rotateRightWithBackWheel())
        mainComm.waitForAnswer()
    if key == ord('l'):
        mainComm.sendBytes(wheelLogic.rotateLeftWithBackWheel())
        mainComm.waitForAnswer()
    if key == ord('q'):
        break
    #mainComm.sendBytes(wheelLogic.motorsOff())
    #mainComm.waitForAnswer()

