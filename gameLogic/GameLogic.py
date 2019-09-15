import serial
from wheelMovementLogic import WheelMovementLogic
from imageProccessing import vision
import time

class GameLogic:


    def __init__(self, imgHandler):

        self.imgHandler = imgHandler
        self.wheelLogic = WheelMovementLogic.WheelMovementLogic()
        self.ballFound = False


        self.screenMidPointX = 320 ## this should be defined somewhere, screensizeX/2
        self.screenMidPointY = 240 ## this should be defined somewhere, screensizeY/2

        ##TODO
        self.ser = serial.Serial('/dev/ttyACM0')
        self.vision = vision.vision()
        #self.mask = self.imgHandler.getBallMask()


        #self.ballCoordinates = self.vision.detect_ball(self.mask)
        #self.ballDistance = self.imgHandler.getDepth()

        self.ballX, self.ballY = self.imgHandler.get_ball_information()
        ##TODO

    def readBytes(self):
        if self.ser.in_waiting:
            line = self.ser.readline().decode("ascii")
            return line.split(":")
        return []

    def waitForAnswer(self):
        msg = self.readBytes()
        for i in range(1000000):
            if len(msg) > 0:
                return msg
            msg = self.readBytes()
        print("Mainboard crashed.")
        return msg

    ##TODO
    def rotateToFindBall(self):
        rotateSpeed = 10
        while 1:
            self.ballX, self.ballY = self.imgHandler.get_ball_information()
            if self.screenMidPointX-5 <= self.ballX <= self.screenMidPointX+5:
                self.ser.write("sd:0:0:0\r\n".encode("utf-8"))
                self.ballFound = True

            if self.screenMidPointX+200 <= self.ballX:
                self.ser.write(self.wheelLogic.rotateLeft(rotateSpeed).encode("utf-8"))
            elif self.screenMidPointX-200 <= self.ballX:
                self.ser.write(self.wheelLogic.rotateRight(rotateSpeed).encode("utf-8"))
            else:
                self.ser.write(self.wheelLogic.rotateLeft(rotateSpeed).encode("utf-8"))

            if self.screenMidPointX+50 <= self.ballX:
                rotateSpeed = 5
            elif self.screenMidPointX-50 <= self.ballX:
                rotateSpeed = 5



            self.waitForAnswer()
            if self.ballFound:
                break
    ##TODO



    def run(self):

        while 1:
            print("siin")

            if not self.ballFound:
                self.rotateToFindBall()


            if self.imgHandler.gameStopped:
                break







