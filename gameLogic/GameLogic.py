import serial
from wheelMovementLogic import WheelMovementLogic
from mainboardCommunication import MainboardCommunication
class GameLogic:


    def __init__(self, imgHandler, mainComm):

        self.imgHandler = imgHandler
        self.wheelLogic = WheelMovementLogic.WheelMovementLogic()
        self.mainComm = mainComm
        self.ballFound = False


        self.screenMidPointX = 320 ## this should be defined somewhere, screensizeX/2
        self.screenMidPointY = 240 ## this should be defined somewhere, screensizeY/2



        self.ballX = 0


    ##TODO
    def rotateToFindBall(self):
        rotateSpeed = 10
        while not self.ballFound:
            self.ballX = self.imgHandler.get_ballX()

            if self.screenMidPointX+100 <= self.ballX:
                self.mainComm.sendBytes(self.wheelLogic.rotateLeft(rotateSpeed))
                self.mainComm.waitForAnswer()
            elif self.screenMidPointX-100 >= self.ballX:
                self.mainComm.sendBytes(self.wheelLogic.rotateRight(rotateSpeed))
                self.mainComm.waitForAnswer()
            else:
                self.mainComm.sendBytes(self.wheelLogic.rotateLeft(rotateSpeed))
                self.mainComm.waitForAnswer()

            if self.screenMidPointX+50 <= self.ballX:
                rotateSpeed = 5
            elif self.screenMidPointX-50 <= self.ballX:
                rotateSpeed = 5

            if self.screenMidPointX-5 <= self.ballX <= self.screenMidPointX+5:
                self.mainComm.sendBytes(self.wheelLogic.motorsOff())
                self.mainComm.waitForAnswer()
                self.ballFound = True

            if self.imgHandler.gameStopped:
                break
    ##TODO



    def run(self):

        while not self.imgHandler.gameStopped:

            if not self.ballFound:
                self.rotateToFindBall()








