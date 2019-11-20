from wheelMovementLogic import WheelMovementLogic
from imageProccessing import ImageProcessing
from mainboardCommunication import MainboardCommunication
import threading
import time


wheelLogic = WheelMovementLogic.WheelMovementLogic()
imageHandler = ImageProcessing.ImageProccessing()

mainComm = MainboardCommunication.MainboardCommunication('/dev/ttyACM0',imageHandler)



#mainboardThread = threading.Thread(target=mainComm.run)
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
#mainboardThread.start()
time.sleep(2)
#mainComm.sendBytes('d:125')

while 1:
    key = imageHandler.key
    time.sleep(0.1)
    omega = wheelLogic.calculateOmega(0.074)
    if key == ord('w'):
        #mainComm.setMotorSpeeds(wheelLogic.setSpeed(90,0,0.06))
        mainComm.sendBytes(wheelLogic.setSpeed(90, 0, 0.06))
        mainComm.waitForAnswer()
    if key == ord("s"):
        #mainComm.setMotorSpeeds(wheelLogic.setSpeed(270,0,0.06))
        mainComm.sendBytes(wheelLogic.setSpeed(270, 0, 0.06))
        mainComm.waitForAnswer()
    if key == ord("a"):
        #mainComm.setMotorSpeeds(wheelLogic.setSpeed(0,-6.4,0.06))
        mainComm.sendBytes(wheelLogic.setSpeed(0, -6.4, 0.06))
        mainComm.waitForAnswer()
    if key == ord("d"):
        #mainComm.setMotorSpeeds(wheelLogic.setSpeed(180,0,0.06))
        mainComm.sendBytes(wheelLogic.setSpeed(180, 0, 0.06))
        mainComm.waitForAnswer()
    if key == ord("c"):
        #mainComm.setMotorSpeeds(wheelLogic.rotateLeft(10))
        mainComm.sendBytes(wheelLogic.rotateLeft(10))
        mainComm.waitForAnswer()
    if key == ord("v"):
        #mainComm.setMotorSpeeds(wheelLogic.rotateRight(10))
        mainComm.sendBytes(wheelLogic.rotateRight(10))
        mainComm.waitForAnswer()
    if key == ord('k'):
        #mainComm.setThrowerSpeed('d:200')
        mainComm.sendBytes('d:200')
    if key == ord('l'):
        mainComm.sendBytes('d:125')
    if key == ord('q'):
        mainComm.closeSerial()
        break
