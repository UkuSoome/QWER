from wheelMovementLogic import WheelMovementLogic
from refHandler import RefHandler
import math
import time
class GameLogic:


    def __init__(self, imgHandler, mainComm, threading):

        self.imgHandler = imgHandler
        self.wheelLogic = WheelMovementLogic.WheelMovementLogic() ## 0.023 seda muuda otse sõitmise kiiruse muutmiseks, 0.05-0.1, 0.1 on suht kiire juba
        self.mainComm = mainComm
        self.threading = threading
        self.ballFound = True
        self.ballReached = False
        self.basketCentered = False
        self.ballCentred = False
        self.ballSideWays = False
        self.BOB = 0

        self.ballDistance = 0
        self.gameState = "PLAY"
        self.refHandler = RefHandler.RefHandler('0', '0',mainComm)
        self.screenMidPointX = 382 ##screenX/2
        self.screenMidPointY = 240 ##screenY/2

        self.basketX = 0
        self.ballX = 0
        self.ballY = 0
    def mainboardThread(self):
        mainCommThread = self.threading.Thread()
        mainCommThread.start()
    def run(self):
        time.sleep(2)
        self.mainComm.sendBytes('d:125')
        #self.mainboardThread()
        while 1:
            #if not self.ballFound:
            #    self.rotateToFindBall()
            #self.readMb()
            if self.gameState == "PLAY":
                if not self.ballFound:
                    self.rotateToFindBall(10)
                if self.ballFound and not self.ballReached:
                    self.driveToBall()
                if self.ballReached and not self.ballCentred:
                    self.centreTheBall(10)
                if self.ballCentred and not self.basketCentered:
                    self.centreTheBasket()

                #if not self.screenMidPointX-20 <= self.ballX <= self.screenMidPointX +20:
                #    self.ballCentred = False
                if self.basketCentered:
                    self.throwTheball()
            if self.imgHandler.gameStopped:
                self.mainComm.sendBytes(self.wheelLogic.motorsOff())
                self.mainComm.waitForAnswer()
                self.mainComm.closeSerial()
                break



    def rotateToFindBall(self,speed):
        #self.readMb()
        self.ballX = self.imgHandler.get_ballX()
        #self.mainComm.sendBytes('d:200')
        if self.screenMidPointX - 5 <= self.ballX <= self.screenMidPointX + 5:
            self.mainComm.sendBytes(self.wheelLogic.motorsOff())
            self.mainComm.waitForAnswer()
            self.ballFound = True
            return

        if self.ballX <= self.screenMidPointX+300:
            speed = 6
            self.mainComm.sendBytes(self.wheelLogic.rotateLeft(speed))
        elif self.screenMidPointX-300 <= self.ballX:
            speed = 6
            self.mainComm.sendBytes(self.wheelLogic.rotateRight(speed))
        elif not self.screenMidPointX-300 <= self.ballX and not self.ballX <= self.screenMidPointX+300:
            self.mainComm.sendBytes(self.wheelLogic.rotateLeft(speed))
        self.mainComm.waitForAnswer()

    def centreTheBall(self,speed):
        #self.readMb()
        ballX = self.imgHandler.get_ballX()
        if self.screenMidPointX - 20 <= ballX <= self.screenMidPointX + 20:
            print("ball centred")
            self.mainComm.sendBytes(self.wheelLogic.motorsOff())
            self.mainComm.waitForAnswer()
            self.ballCentred = True
            return

        if ballX <= self.screenMidPointX+300:
            self.mainComm.sendBytes(self.wheelLogic.rotateLeft(speed))
            self.mainComm.waitForAnswer()
        elif ballX >= self.screenMidPointX-300:
            self.mainComm.sendBytes(self.wheelLogic.rotateRight(speed))
            self.mainComm.waitForAnswer()


    def driveToBall(self):
        #self.readMb()
        angle = self.calculateAngleToBall()
        if self.ballY >= 450:
            print("jõudsin pallini")
            self.mainComm.sendBytes(self.wheelLogic.motorsOff())
            self.mainComm.waitForAnswer()
            self.ballReached = True
            if self.BOB == 0:
                time.sleep(0.5)
            return

        if self.ballX <= self.screenMidPointX:
            self.mainComm.sendBytes(self.wheelLogic.setSpeed(90 + angle,0,0.08))
        elif self.ballX >= self.screenMidPointX:
            self.mainComm.sendBytes(self.wheelLogic.setSpeed(90 - angle,0,0.08))
        self.mainComm.waitForAnswer()



    def calculateAngleToBall(self):
        ballY = self.imgHandler.get_ballY()
        ballX = self.imgHandler.get_ballX()
        a = abs(ballY - self.screenMidPointY)
        c = self.screenMidPointX * 2 - ballX
        angle = math.degrees(math.atan(a / c))
        return int(angle)

    def centreTheBasket(self):
        #self.readMb()
        basketX = self.imgHandler.get_basketX()
        print(basketX)
        if self.screenMidPointX - 5 <= basketX <= self.screenMidPointX + 5:
            print("korv keskel")
            self.mainComm.sendBytes(self.wheelLogic.motorsOff())

            self.mainComm.waitForAnswer()
            self.basketCentered = True
            return
        omega = self.wheelLogic.calculateOmega(0.074)
        if self.screenMidPointX-300 <= self.basketX:
            self.mainComm.sendBytes(self.wheelLogic.setSpeed(180,-10,omega,0.019))
        elif self.screenMidPointX+300 >= self.basketX:
            self.mainComm.sendBytes(self.wheelLogic.setSpeed(180,-10,omega,0.019))
        else:
            self.mainComm.sendBytes(self.wheelLogic.setSpeed(180,-10,omega,0.023))
        self.mainComm.waitForAnswer()
        if self.BOB == 200:
            self.ballReached = False
            self.ballCentred = False
            self.BOB = 0
            if self.ballY >= 470:
                self.wheelLogic.setSpeed(270,-10,1,0.010)
        self.BOB += 1

    def throwTheball(self):
        #self.readMb()
        starttime = time.time()
        while time.time() - starttime < 1.3:
            self.mainComm.sendBytes('d:200')
            self.mainComm.sendBytes(self.wheelLogic.setSpeed(90,-30,1,0.023))
            self.mainComm.waitForAnswer()

        self.ballReached = False
        self.basketCentered = False
        self.ballCentred = False
        self.ballFound = False
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









