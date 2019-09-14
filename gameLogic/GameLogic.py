import serial
from wheelMovementLogic import WheelMovementLogic
from imageProccessing import vision

class GameLogic:


    def __init__(self, imgHandler):

        ##muuutujad

        self.imgHandler = imgHandler
        self.wheelLogic = WheelMovementLogic.WheelMovementLogic()
        self.ballFound = False


        self.screenMidPointX = 320 ## this should be defined somewhere, screensizeX/2
        self.screenMidPointY = 240 ## this should be defined somewhere, screensizeY/2

        ##TODO
        self.ser = serial.Serial('/dev/ttyACM0')
        self.vision = vision.vision()
        self.mask = self.imgHandler.getBallMask()
        self.ballCoordinates = self.vision.detect_ball(self.mask)
        self.ballX = self.ballCoordinates ## todo
        self.ballDistance = self.imgHandler.getDepth()
        ##TODO

    ##TODO
    def rotateToFindBall(self):
        while not self.ballFound:
            self.ser.write(self.wheelLogic.rotateLeft(20).encode("utf-8"))
            while self.ser.out_waiting != 0:
                pass
    ##TODO



    def run(self):

        while 1:
            if not self.ballFound:
                self.rotateToFindBall()







