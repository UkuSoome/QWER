from wheelMovementLogic import WheelMovementLogic
from imageProccessing import ImageProcessing
from mainboardCommunication import MainboardCommunication
import threading
import time
import signal
TIMEOUT = 1 # number of seconds your want for timeout


wheelLogic = WheelMovementLogic.WheelMovementLogic()
imageHandler = ImageProcessing.ImageProccessing()

mainComm = MainboardCommunication.MainboardCommunication('/dev/ttyACM0',imageHandler)



#mainboardThread = threading.Thread(target=mainComm.run)
imageThread = threading.Thread(target=imageHandler.run)

kaugustedict = {
  ###kaugus: ###kiirus
    0.52835:145,
    0.66035:146,
    0.71710:147,
    0.7490999999999999:148,
    0.79115:149,
    0.86795:150,
    0.91935:151,
    0.9582499999999999:152,
    0.9871:153,
    1.0429499999999998:154,
    1.15525:155,
    1.195:156,
    1.2552999999999999:157,
    1.37745:158,
    1.4281499999999998:159,
    1.4906:160,
    1.5572:161,
    1.69785:162,
    1.74905:163,
    1.853:164,
    1.98575:165,
    2.0915:166,
    2.1749:167,
    2.4117499999999996:168,
    2.4734:169,
    2.52192:170,
    2.67335:171,
    2.7086:172,
    2.7059:173,
    2.7271:175,
    2.74585:176,
    2.76965:177,
    2.8584499999999997:178,
    2.9413000000000006:179,
    3.0846:180,
    3.1465:181,
    3.2321:182,
    3.4512:183,
    3.58795:184,
    3.65775:185,
    3.7645:186,
    3.8257:187,
    3.8855:188,
    3.94654:189,
    4.004:190,
    4.0837:191,
    4.12295:192,
    4.17895:193,
    4.2365:194,
    4.28:195,
    4.30895:196,
    4.38295:197,
    4.4091:198,
    4.4596:199,
    4.5343:200,
}
imageThread.start()
#mainboardThread.start()
time.sleep(2)
#mainComm.sendBytes('d:125')
korgus = 0.232
kaugus = 0.137
c = 0.271


def throwTheball(kiirus):

    print(imageHandler.getBasketDistance())
    starttime = time.time()
    while time.time() - starttime < 2:
        # self.mainComm.setThrowerSpeed('d:160')
        # self.mainComm.setMotorSpeeds(self.wheelLogic.setSpeed(90,0,0.03))
        mainComm.sendBytes('d:'+str(kiirus))
        time.sleep(0.1)
        mainComm.sendBytes(wheelLogic.setSpeed(90, 0, 0.03))
        mainComm.waitForAnswer()

    mainComm.sendBytes('d:125')
while 1:
    key = imageHandler.key
    time.sleep(0.1)
    if key == ord('w'):
        #mainComm.setMotorSpeeds(wheelLogic.setSpeed(90,0,0.06))
        mainComm.sendBytes(wheelLogic.setSpeed(90, 0, 0.06))
        mainComm.waitForAnswer()
    if key == ord("s"):
        #mainComm.setMotorSpeeds(wheelLogic.setSpeed(270,0,0.06))
        mainComm.sendBytes(wheelLogic.setSpeed(270, 0, 0.06))
        mainComm.waitForAnswer()
    if key == ord("a"):
        mainComm.sendBytes(wheelLogic.setSpeed(0, 0, 0.03))
        mainComm.waitForAnswer()
    if key == ord("d"):
        #mainComm.setMotorSpeeds(wheelLogic.setSpeed(180,0,0.06))
        mainComm.sendBytes(wheelLogic.setSpeed(180, 0, 0.03))
        mainComm.waitForAnswer()
    if key == ord("c"):
        #mainComm.setMotorSpeeds(wheelLogic.rotateLeft(10))
        mainComm.sendBytes(wheelLogic.rotateLeft(0.15))
        mainComm.waitForAnswer()
    if key == ord("v"):
        #mainComm.setMotorSpeeds(wheelLogic.rotateRight(10))
        mainComm.sendBytes(wheelLogic.rotateRight(0.15))
        mainComm.waitForAnswer()
    if key == ord('k'):
        throwTheball(200)
    if key == ord('l'):
        mainComm.sendBytes('d:125')
    if key == ord('q'):
        mainComm.closeSerial()
        break
