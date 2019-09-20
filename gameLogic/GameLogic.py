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

        self.screenMidPointX = 320 ## this should be defined somewhere, screensizeX/2
        self.screenMidPointY = 240 ## this should be defined somewhere, screensizeY/2



        self.ballX = 0
        self.ballY = 0


    ##TODO
    def rotateToFindBall(self):
        while not self.ballFound:
            self.ballX = self.imgHandler.get_ballX()

            if self.screenMidPointX - 15 <= self.ballX <= self.screenMidPointX + 15:
                print("leidsin palli")
                self.mainComm.sendBytes(self.wheelLogic.motorsOff())
                self.mainComm.waitForAnswer()
                self.ballFound = True
                break

            if self.ballX <= self.screenMidPointX+285:
                rotateSpeed = 7
                self.mainComm.sendBytes(self.wheelLogic.rotateLeft(rotateSpeed))
            elif self.screenMidPointX-315 <= self.ballX:
                rotateSpeed = 7
                self.mainComm.sendBytes(self.wheelLogic.rotateRight(rotateSpeed))
            else:
                rotateSpeed = 15
                self.mainComm.sendBytes(self.wheelLogic.rotateLeft(rotateSpeed))
            self.mainComm.waitForAnswer()



            if self.imgHandler.gameStopped:
                break
    ##TODO

    def driveToBallInAStraightLine(self):
        speed = 10
        while not self.ballReached:
            self.ballX = self.imgHandler.get_ballX()
            self.ballY = self.imgHandler.get_ballY()
            #angle = self.calculateAngleToBall()
            #print(angle)
            print(self.ballY)
            #self.mainComm.sendBytes(self.wheelLogic.setSpeed(-90-angle,speed))
            self.mainComm.sendBytes(self.wheelLogic.setSpeed(-90, speed))

            if self.ballY >= 390:
                print("leidsin palli")
                #self.ballReached = True
            if self.imgHandler.gameStopped:
                break



    def calculateAngleToBall(self):
        a = self.ballY
        c = math.sqrt((640-self.ballX) ** 2 + (480-self.ballY) ** 2)
        angle = math.degrees(math.acos(a / c))
        return int(angle)



    def run(self):
        time.sleep(3)
        while not self.imgHandler.gameStopped:
            if not self.ballFound:
                self.rotateToFindBall()


            #if not self.ballReached:
            #    self.driveToBallInAStraightLine()









