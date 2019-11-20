from wheelMovementLogic import WheelMovementLogic
from refHandler import RefHandler
import math
import time
class GameLogic:


    def __init__(self, imgHandler, mainComm):

        self.imgHandler = imgHandler
        self.wheelLogic = WheelMovementLogic.WheelMovementLogic()
        self.mainComm = mainComm
        self.ballFound = True
        self.ballReached = False
        self.basketCentered = False
        self.ballCentred = False
        self.ballSideWays = False
        self.BOB = 0

        self.ballDistance = 0
        self.gameState = "PLAY"
        self.refHandler = RefHandler.RefHandler('0', '0',mainComm)
        self.screenMidPointX = 320 ##screenX/2
        self.screenMidPointY = 223 ##screenY/2

        self.basketX = 0
        self.basketY = 0
        self.ballX = 0
        self.ballY = 0
    def run(self):
        time.sleep(2)
        while 1:
            if self.gameState == "PLAY":
                if not self.ballFound:
                    self.rotateToFindBall(10)
                if self.ballFound and not self.ballReached:
                    self.driveToBall()
                if self.ballReached and not self.ballCentred:
                    self.centreTheBall(10)
                if self.ballCentred and not self.basketCentered:
                    self.centreTheBasket()
                if not self.screenMidPointY-20 <= self.ballX <= self.screenMidPointY +20:
                    self.ballCentred = False
                if self.basketCentered:
                    self.throwTheball()

            if self.imgHandler.gameStopped:
                #self.mainComm.setMotorSpeeds(self.wheelLogic.motorsOff())
                self.mainComm.sendBytes(self.wheelLogic.motorsOff())
                self.mainComm.waitForAnswer()
                self.mainComm.closeSerial()
                break



    def rotateToFindBall(self,speed):
        self.ballY = self.imgHandler.get_ballY()
        if self.screenMidPointY - 10 <= self.ballY <= self.screenMidPointY + 10:
            print("ball found")
            self.mainComm.sendBytes(self.wheelLogic.motorsOff())
            self.mainComm.waitForAnswer()
            self.ballFound = True
            return

        if self.screenMidPointY + 10 <= self.ballY <= 480:
            self.mainComm.sendBytes(self.wheelLogic.rotateLeft(10))
        elif self.screenMidPointY - 10 >= self.ballY >= 0:
            self.mainComm.sendBytes(self.wheelLogic.rotateRight(10))
        else:
            self.mainComm.sendBytes(self.wheelLogic.rotateRight(10))
        self.mainComm.waitForAnswer()
    def centreTheBall(self,speed):
        self.ballY = self.imgHandler.get_ballY()
        if self.screenMidPointY - 10 <= self.ballY <= self.screenMidPointY + 10:
            print("ball centred")
            #self.mainComm.setMotorSpeeds(self.wheelLogic.motorsOff())
            self.mainComm.sendBytes(self.wheelLogic.motorsOff())
            self.mainComm.waitForAnswer()
            self.ballCentred = True
            return

        if self.screenMidPointY+10 <= self.ballY <= 480:
            #self.mainComm.setMotorSpeeds(self.wheelLogic.rotateLeft(speed))
            self.mainComm.sendBytes(self.wheelLogic.rotateRight(speed))
        elif self.screenMidPointY-10 >= self.ballY >= 0:
            #self.mainComm.setMotorSpeeds(self.wheelLogic.rotateRight(speed))
            self.mainComm.sendBytes(self.wheelLogic.rotateRight(speed))
        else:
            #self.mainComm.setMotorSpeeds(self.wheelLogic.rotateRight(speed))
            self.mainComm.sendBytes(self.wheelLogic.rotateRight(speed))
        self.mainComm.waitForAnswer()



    def driveToBall(self):
        print("siin")
        #self.readMb()
        angle = self.calculateAngleToBall()
        if self.ballX >= 350:
            print("jõudsin pallini")
            #self.mainComm.setMotorSpeeds(self.wheelLogic.motorsOff())
            self.mainComm.sendBytes(self.wheelLogic.motorsOff())
            self.mainComm.waitForAnswer()
            self.ballReached = True
            if self.BOB == 0:
                time.sleep(0.5)
            return
        if self.ballY != -1:
            if self.ballY<= self.screenMidPointY:
                #self.mainComm.setMotorSpeeds(self.wheelLogic.setSpeed(90 + angle,0,0.07))
                self.mainComm.sendBytes(self.wheelLogic.setSpeed(90 + angle,0,0.07))
                self.mainComm.waitForAnswer()
            elif self.ballY >= self.screenMidPointY:
                #self.mainComm.setMotorSpeeds(self.wheelLogic.setSpeed(90 - angle,0,0.07))
                self.mainComm.sendBytes(self.wheelLogic.setSpeed(90 - angle,0,0.07))
                self.mainComm.waitForAnswer()


    def calculateAngleToBall(self):
        self.ballY = self.imgHandler.get_ballY()
        self.ballX = self.imgHandler.get_ballX()
        a = abs(self.ballY - self.screenMidPointY)
        c = 640 - self.ballX
        angle = math.degrees(math.atan(a / c))
        return angle

    def centreTheBasket(self):
        self.basketY = self.imgHandler.get_basketY()
        self.ballY = self.imgHandler.get_ballY()
        if self.screenMidPointY - 5 <= self.basketY <= self.screenMidPointY + 5:
            print("korv keskel")
            #self.mainComm.setMotorSpeeds(self.wheelLogic.motorsOff())
            self.mainComm.sendBytes(self.wheelLogic.motorsOff())
            self.mainComm.waitForAnswer()
            self.basketCentered = True
            return
        omega = self.wheelLogic.calculateOmega(self.ballY/2)
        if self.screenMidPointY-220 <= self.basketY:
            #self.mainComm.setMotorSpeeds(self.wheelLogic.setSpeed(0,omega,0.03))
            self.mainComm.sendBytes(self.wheelLogic.setSpeed(0, omega, 0.03))
        elif self.screenMidPointY+220 >= self.basketY:
            #self.mainComm.setMotorSpeeds(self.wheelLogic.setSpeed(0,omega,0.03))
            self.mainComm.sendBytes(self.wheelLogic.setSpeed(0, omega, 0.03))
        else:
            #self.mainComm.setMotorSpeeds(self.wheelLogic.setSpeed(0,omega,0.03))
            self.mainComm.sendBytes(self.wheelLogic.setSpeed(0, omega, 0.03))
        self.mainComm.waitForAnswer()
        if self.BOB == 200:
            self.ballReached = False
            self.ballCentred = False
            self.BOB = 0
        self.BOB += 1

    def throwTheball(self):
        starttime = time.time()
        while time.time() - starttime < 3:
            #self.mainComm.setThrowerSpeed('d:160')
            #self.mainComm.setMotorSpeeds(self.wheelLogic.setSpeed(90,0,0.03))
            self.mainComm.sendBytes('d:160')
            self.mainComm.sendBytes(self.wheelLogic.setSpeed(90,0,0.03))
            self.mainComm.waitForAnswer()

        self.ballReached = False
        self.basketCentered = False
        self.ballCentred = False
        self.ballFound = False
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









