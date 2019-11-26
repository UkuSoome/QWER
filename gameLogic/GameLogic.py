from wheelMovementLogic import WheelMovementLogic
from refHandler import RefHandler
import math
import time
import numpy as np
class GameLogic:

    def __init__(self, imgHandler, mainComm):

        self.imgHandler = imgHandler
        self.wheelLogic = WheelMovementLogic.WheelMovementLogic()
        self.mainComm = mainComm
        self.ballFound = False
        self.ballReached = False
        self.basketCentered = False
        self.ballCentred = False
        self.ballSideWays = False
        self.ballDistanced = False
        self.BOB = 0
        self.ballDistance = 0
        self.gameState = "PLAY"
        self.refHandler = RefHandler.RefHandler('B', 'B',mainComm)
        self.screenMidPointX = 320 ##screenX/2
        self.screenMidPointY = 229 ##screenY/2

        self.rotationsDone = 0

        self.basketX = 0
        self.basketY = 0
        self.ballX = 0
        self.ballY = 0
        self.countt = 0
        self.kaugused = {
            ###kaugus: ###kiirus
            0.52835: 145,
            0.66035: 146,
            0.6976999999999998:147,
            0.71710: 147,
            0.7186:147,
            0.7490999999999999: 148,
            0.78285:148,
            0.79115: 149,
            0.79825:149,
            0.86795: 150,
            0.88275: 150,
            0.88615:150,
            0.902:150,
            0.92465:150,
            0.93795:150,
            0.95825:151,
            0.9504:151,
            0.965:151,
            0.97565:151,
            0.97895:151,
            0.9813:151,
            0.9865:151,
            1.02655:151,
            1.02915:151,
            1.373:152,
            1.0644:153,
            1.09345:153,
            1.10825:153,
            1.13434:153,
            1.1366:153,
            1.14135:153,
            1.17055:154,
            1.1860:155,
            1.2271:155,
            1.2275:155,
            1.23205:156,
            1.2613:156,
            1.26565:156,
            1.2629:156,
            1.2712:156,
            1.2901:156,
            1.30755:156,
            1.3255:157,
            1.3364:157,
            1.4242:157,
            1.4467:158,
            1.4471:158,
            1.475:158,
            1.5087:159,
            1.5275:160,
            1.553:159,
            1.5571:160,
            1.6753:160,
            1.74585:162,
            1.76055:162,
            1.80865:162,
            1.86485:162,
            1.9182:162,
            1.9982:163,
            2.0402:163,
            2.06544:163,
            2.09435:163,
            2.1483000000000043:163,
            2.1875:163,
            2.22845:169,
            2.26545:169,
            2.28615:169,
            2.31835:170,
            2.39215:172,
            2.49354:173,
            2.5123:176,
            2.54025:176,
            2.64:176,
            2.7172:182,
            2.9177:181,
            3.1465: 181,
            3.2321: 181,
            3.4512: 184,
            3.58795: 184,
            3.65775: 185,
            3.7645: 190,
            3.94654: 190,
            4.004: 190,
            4.0837: 191,
            4.12295: 192,
            4.1653:195,
            4.2365: 195,
            4.28: 195,
            4.30895: 198,
            4.4596: 199,
            4.5343: 200,
            4.6036:211,
            4.71505:213,
            4.83526:214,
        }
    def run(self):
        time.sleep(2)
        while 1:
            if self.gameState == "PLAY":
                if not self.ballFound:
                    self.rotateToFindBall()
                if self.ballFound and not self.ballReached:
                    self.driveToBall()
                if self.ballReached and not self.ballCentred:
                    self.centreTheBall()
                if self.ballCentred and not self.basketCentered:
                    self.centreTheBasket()
                if self.basketCentered and not self.ballDistanced:
                    self.adjustDistance()
                if self.ballDistanced:
                    self.throwTheball()
            else:
                self.readMb()

            if self.imgHandler.gameStopped:
                #self.mainComm.setMotorSpeeds(self.wheelLogic.motorsOff())
                self.mainComm.waitForAnswer()
                self.mainComm.sendBytes(self.wheelLogic.motorsOff())
                self.mainComm.waitForAnswer()
                self.mainComm.closeSerial()
                break

    def adjustDistance(self):

        self.ballDistance = self.imgHandler.getBallDistance()
        if  self.ballDistance <= 0.3:
            print("palli kaugus")
            self.mainComm.sendBytes(self.wheelLogic.motorsOff())
            self.mainComm.waitForAnswer()
            self.ballDistanced = True
            return
        if 0.3 <= self.ballDistance <= 3:
            self.mainComm.sendBytes(self.wheelLogic.setSpeed(90,0,0.01))
            self.mainComm.waitForAnswer()
        elif self.ballDistance == -1:
            self.ballFound = False
            self.ballReached = False
            self.ballCentred = False
    def rotateToFindBall(self):
        self.ballY = self.imgHandler.get_ballY()
        if self.ballY != -1:
            print("ball found")
            self.mainComm.sendBytes(self.wheelLogic.motorsOff())
            self.mainComm.waitForAnswer()
            self.ballFound = True
            starttime = time.time()
            while time.time() - starttime < 0.25:
                pass
            return
        else:
            self.mainComm.sendBytes(self.wheelLogic.rotateRight(0.45))
            self.mainComm.waitForAnswer()
            if self.BOB == 200:
                self.basketY = self.imgHandler.get_basketY()
                self.mainComm.sendBytes(self.wheelLogic.motorsOff())
                self.mainComm.waitForAnswer()
                starttime = time.time()
                while time.time() - starttime < 0.10:
                    pass
                self.BOB = 0
                self.rotationsDone += 1

                if self.rotationsDone > 7 and self.basketY != -1:
                    self.mainComm.sendBytes(self.wheelLogic.motorsOff())
                    self.mainComm.waitForAnswer()
                    while time.time() - starttime < 1:
                        pass
                    for i in range(300):
                        self.driveTowardsOwnBasket()
                    self.rotationsDone = 0
            self.BOB += 1



    def centreTheBall(self):
        self.ballY = self.imgHandler.get_ballY()
        self.basketY = self.imgHandler.get_basketY()
        if self.screenMidPointY -5 <= self.ballY <= self.screenMidPointY + 5:
            print("ball centred")
            #self.mainComm.setMotorSpeeds(self.wheelLogic.motorsOff())
            self.mainComm.sendBytes(self.wheelLogic.motorsOff())
            self.mainComm.waitForAnswer()
            self.ballCentred = True
            return
        speed = 0.09
        if self.basketY != -1:
            if 150 <= self.basketY <= 290:
                speed = 0.03
        if self.screenMidPointY+5 <= self.ballY <= 480:
            #self.mainComm.setMotorSpeeds(self.wheelLogic.rotateLeft(speed))
            self.mainComm.sendBytes(self.wheelLogic.rotateLeft(speed))
            self.mainComm.waitForAnswer()
        elif self.screenMidPointY-5 >= self.ballY >= 0:
            #self.mainComm.setMotorSpeeds(self.wheelLogic.rotateRight(speed))
            self.mainComm.sendBytes(self.wheelLogic.rotateRight(speed))
            self.mainComm.waitForAnswer()
        else:
            self.BOB += 1
            if self.BOB == 500:
                self.ballFound = False
                self.ballReached = False
                self.BOB = 0
    def calculateAngleToBasket(self,n):
        self.basketY = self.imgHandler.get_basketY()
        self.basketX = self.imgHandler.get_basketY()
        a = abs(self.basketY - self.screenMidPointY+n)
        c = 640 - self.basketX
        angle = math.degrees(math.atan(a / c))
        return angle
    def driveTowardsOwnBasket(self):
        angle = self.calculateAngleToBasket(0)
        if self.basketY <= self.screenMidPointY:
            # self.mainComm.setMotorSpeeds(self.wheelLogic.setSpeed(90 + angle,0,0.07))
            self.mainComm.sendBytes(self.wheelLogic.setSpeed(90 + angle, 0, 0.18))
            self.mainComm.waitForAnswer()
        elif self.basketY >= self.screenMidPointY:
            # self.mainComm.setMotorSpeeds(self.wheelLogic.setSpeed(90 - angle,0,0.07))
            self.mainComm.sendBytes(self.wheelLogic.setSpeed(90 - angle, 0, 0.18))
            self.mainComm.waitForAnswer()

    def driveToBall(self):
        #self.readMb()
        angle = self.calculateAngleToBall()
        if self.ballX >= 280:
            print("jõudsin pallini")
            #self.mainComm.setMotorSpeeds(self.wheelLogic.motorsOff())
            self.mainComm.sendBytes(self.wheelLogic.motorsOff())
            self.mainComm.waitForAnswer()
            self.ballReached = True
            if self.BOB == 0:
                time.sleep(0.1)
            return
        self.ballY = self.imgHandler.get_ballY()
        if self.ballY != -1:
            if self.ballY<= self.screenMidPointY:
                #self.mainComm.setMotorSpeeds(self.wheelLogic.setSpeed(90 + angle,0,0.07))
                self.mainComm.sendBytes(self.wheelLogic.setSpeed(90 + angle,0,0.18))
                self.mainComm.waitForAnswer()
            elif self.ballY >= self.screenMidPointY:
                #self.mainComm.setMotorSpeeds(self.wheelLogic.setSpeed(90 - angle,0,0.07))
                self.mainComm.sendBytes(self.wheelLogic.setSpeed(90 - angle,0,0.18))
                self.mainComm.waitForAnswer()
        else:
            self.ballFound = False


    def calculateAngleToBall(self):
        self.ballY = self.imgHandler.get_ballY()
        self.ballX = self.imgHandler.get_ballX()
        a = abs(self.ballY - self.screenMidPointY)
        c = 640 - self.ballX
        angle = math.degrees(math.atan(a / c))
        return angle

    def centreTheBasket(self):
        self.basketY = self.imgHandler.get_basketY()
        self.basketX = self.imgHandler.get_basketY()
        self.ballY = self.imgHandler.get_ballY()
        omega = self.wheelLogic.calculateOmega(0.068)
        if self.screenMidPointY+12 <= self.basketY <= self.screenMidPointY + 20:
            self.BOB += 1
            self.mainComm.sendBytes(self.wheelLogic.motorsOff())
            self.mainComm.waitForAnswer()
            if self.BOB > 15:
                self.basketCentered = True
                self.BOB = 0
            return
        speed = 0.05
        self.basketY = self.imgHandler.get_basketY()
        if self.basketY != -1:
            if 150 <= self.basketY <= 290:
                speed = 0.015
            if 0 <= self.basketY < self.screenMidPointY+12:
                #self.mainComm.setMotorSpeeds(self.wheelLogic.setSpeed(0,omega,0.03))
                self.mainComm.sendBytes(self.wheelLogic.setSpeed(0, omega, speed))
            elif self.screenMidPointY +20 <= self.basketY <= 480:
                #self.mainComm.setMotorSpeeds(self.wheelLogic.setSpeed(0,omega,0.03))
                self.mainComm.sendBytes(self.wheelLogic.setSpeed(180, -omega, speed))
        else:
            #self.mainComm.setMotorSpeeds(self.wheelLogic.setSpeed(0,omega,0.03))
            self.mainComm.sendBytes(self.wheelLogic.setSpeed(0, omega, 0.07))
        self.mainComm.waitForAnswer()
        if self.BOB == 150:
            self.ballReached = False
            self.ballCentred = False
            self.BOB = 0
        self.BOB += 1

    def throwTheball(self):
        timenow = time.time()
        while time.time() - timenow <= 0.2:
            pass
        print("viskan palli")
        basketDistance = 0
        for i in range(500):
            basketDistance+=self.imgHandler.getBasketDistance()
        basketDistance = basketDistance / 500
        #throwerSpeed = 4.5039*(basketDistance**3) - 16.398*(basketDistance**2) + 28.18*basketDistance + 140.6
        throwerSpeed = self.kaugused.get(basketDistance, self.kaugused[min(self.kaugused.keys(), key=lambda k: abs(k - basketDistance))])
        print(throwerSpeed)
        print(basketDistance)
        starttime = time.time()
        while time.time() - starttime <= 2.5:
            angle = self.calculateAngleToBasket(15)
            self.mainComm.sendBytes('d:'+str(int(throwerSpeed)))
            if self.basketY <= self.screenMidPointY+30:
                self.mainComm.sendBytes(self.wheelLogic.setSpeed(90 + angle, 0, 0.03))
                self.mainComm.waitForAnswer()
            elif self.basketY >= self.screenMidPointY+25:
                self.mainComm.sendBytes(self.wheelLogic.setSpeed(90 - angle, 0, 0.03))
                self.mainComm.waitForAnswer()

        self.ballReached = False
        self.basketCentered = False
        self.ballCentred = False
        self.ballFound = False
        self.ballDistanced = False
        #self.mainComm.setThrowerSpeed('d:125')
        self.mainComm.sendBytes('d:125')

    def handleMbCommands(self, msg):
        if msg != None:
            command = msg[0]
            print(msg)
            if command == "<ref":
                cmd = self.refHandler.handleMsg(msg[1])
                print(cmd)
                if cmd == "START":
                    self.gameState = "PLAY"

                if cmd == "STOP":
                    self.gameState = "STOP"

                if cmd == "PING":
                    print("Sending ACK")

    def readMb(self):
        mbMsg = self.mainComm.readBytes()
        if len(mbMsg) > 0:
            self.handleMbCommands(mbMsg)









