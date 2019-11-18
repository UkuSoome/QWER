from wheelMovementLogic import WheelMovementLogic
from imageProccessing import ImageProcessing
from mainboardCommunication import MainboardCommunication
import threading
import time


wheelLogic = WheelMovementLogic.WheelMovementLogic()

mainComm = MainboardCommunication.MainboardCommunication('/dev/ttyACM0')


imageHandler = ImageProcessing.ImageProccessing()



imageThread = threading.Thread(target=imageHandler.run)

kaugustedict = {
  ###kaugus: ###kiirus
    0.56:147,
    0.84:150,
    1.10:155,
    1.52:160,
    1.93:165,
    2.29:170,
}
imageThread.start()
time.sleep(2)
mainComm.sendBytes('d:125')
while 1:
    key = imageHandler.key
    time.sleep(0.1)
    omega = wheelLogic.calculateOmega(0.074)
    if key == ord('w'):
        mainComm.sendBytes(wheelLogic.setSpeed(90,1,0.06))
        mainComm.waitForAnswer()
    if key == ord("s"):
        mainComm.sendBytes(wheelLogic.setSpeed(270,1,0.06))
        mainComm.waitForAnswer()
    if key == ord("a"):
        mainComm.sendBytes(wheelLogic.setSpeed(0,omega,0.06))
        mainComm.waitForAnswer()
    if key == ord("d"):
        mainComm.sendBytes(wheelLogic.setSpeed(180,10,0.06))
        mainComm.waitForAnswer()
    if key == ord("c"):
        mainComm.sendBytes(wheelLogic.rotateLeft(10))
        mainComm.waitForAnswer()
    if key == ord("v"):
        mainComm.sendBytes(wheelLogic.rotateRight(10))
        mainComm.waitForAnswer()
    if key == ord('k'):
        mainComm.sendBytes('d:200')
    if key == ord('l'):
        mainComm.sendBytes('d:125')
    if key == ord('q'):
        break
    #mainComm.sendBytes(wheelLogic.motorsOff())
    #mainComm.waitForAnswer()
