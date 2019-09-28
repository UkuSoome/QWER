from wheelMovementLogic import WheelMovementLogic
import math
import time
class GameLogic:


    def __init__(self, imgHandler, mainComm):

        self.imgHandler = imgHandler
        self.wheelLogic = WheelMovementLogic.WheelMovementLogic()
        self.mainComm = mainComm
        self.ballFound = False
        self.ballReached = False
        self.basketCentered = False
        self.ballCentred = False

        self.screenMidPointX = 320 ##screenX/2
        self.screenMidPointY = 240 ##screenY/2

        self.basketX = 0
        self.ballX = 0
        self.ballY = 0


    ##TODO
    def rotateToFindBall(self):
        self.ballX = self.imgHandler.get_ballX()

        if self.screenMidPointX - 15 <= self.ballX <= self.screenMidPointX + 15:
            print("leidsin palli")
            self.mainComm.sendBytes(self.wheelLogic.motorsOff())
            self.mainComm.waitForAnswer()
            self.ballFound = True
            return

        if self.ballX <= self.screenMidPointX+300:
            rotateSpeed = 8
            self.mainComm.sendBytes(self.wheelLogic.rotateLeft(rotateSpeed))
        elif self.screenMidPointX-300 <= self.ballX:
            rotateSpeed = 8
            self.mainComm.sendBytes(self.wheelLogic.rotateRight(rotateSpeed))
        elif not self.screenMidPointX-300 <= self.ballX and not self.ballX <= self.screenMidPointX+300:
            rotateSpeed = 20
            self.mainComm.sendBytes(self.wheelLogic.rotateLeft(rotateSpeed))

        self.mainComm.waitForAnswer()

    def centreTheBall(self):
        ballX = self.imgHandler.get_ballX()
        rotateSpeed = 5
        if self.screenMidPointX - 1 <= ballX <= self.screenMidPointX + 1:
            print("ball centred")
            self.mainComm.sendBytes(self.wheelLogic.motorsOff())
            self.mainComm.waitForAnswer()
            self.ballCentred = True
            return

        if ballX <= self.screenMidPointX+300:
            self.mainComm.sendBytes(self.wheelLogic.rotateLeft(rotateSpeed))
            self.mainComm.waitForAnswer()
        elif ballX >= self.screenMidPointX-300:
            self.mainComm.sendBytes(self.wheelLogic.rotateRight(rotateSpeed))
            self.mainComm.waitForAnswer()

    ##TODO

    def driveToBall(self):
        speed = 50
        angle = self.calculateAngleToBall()

        if self.ballY >= 400:
            print("jõudsin pallini")
            self.mainComm.sendBytes(self.wheelLogic.motorsOff())
            self.mainComm.waitForAnswer()
            self.ballReached = True
            return

        if self.ballX <= self.screenMidPointX:
            self.mainComm.sendBytes(self.wheelLogic.setSpeed(-90 + angle, speed))
        elif self.ballX >= self.screenMidPointX:
            self.mainComm.sendBytes(self.wheelLogic.setSpeed(-90 - angle, speed))
        self.mainComm.waitForAnswer()



    def calculateAngleToBall(self):
        self.ballY = self.imgHandler.get_ballY()
        self.ballX = self.imgHandler.get_ballX()
        a = abs(self.ballX - self.screenMidPointX)
        c = self.screenMidPointY * 2 - self.ballY
        angle = math.degrees(math.atan(a / c))
        return int(angle)

    def centreTheBasket(self):
        basketX = self.imgHandler.get_basketX()
        print(basketX)
        if self.screenMidPointX - 3 <= basketX <= self.screenMidPointX + 3:
            print("korv keskel")
            self.mainComm.sendBytes(self.wheelLogic.motorsOff())
            self.mainComm.waitForAnswer()
            self.basketCentered = True
            return

        if basketX < self.screenMidPointX:
            self.mainComm.sendBytes(self.wheelLogic.rotateRightWithBackWheel())
        elif basketX > self.screenMidPointX:
            self.mainComm.sendBytes(self.wheelLogic.rotateLeftWithBackWheel())
        self.mainComm.waitForAnswer()

    def throwTheball(self):
        self.mainComm.sendBytes('d:200')
        self.mainComm.sendBytes(self.wheelLogic.setSpeed(90,-20))
        self.mainComm.waitForAnswer()


    def run(self):
        time.sleep(2)
        self.mainComm.sendBytes('d:125')
        while 1:
            #if not self.ballFound:
            #    self.rotateToFindBall()
            if not self.ballReached:# and self.ballFound:
                self.driveToBall()
            if self.ballReached and not self.ballCentred:
                self.centreTheBall()
            if self.ballCentred and not self.basketCentered:
                self.centreTheBasket()
            if self.basketCentered:
                self.throwTheball()


            if self.imgHandler.gameStopped:
                self.mainComm.sendBytes(self.wheelLogic.motorsOff())
                self.mainComm.waitForAnswer()
                self.mainComm.closeSerial()
                break










