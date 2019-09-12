
import math



class WheelMovementLogic:


    def __init__(self):

        self.wheelOneAngle = 240 ## this should be 0
        self.wheelTwoAngle = 120
        self.wheelThreeAngle = 0 ## this should be 240

    def rotateLeft(self):
        return "sd:10:10:10\r\n"

    def rotateRight(self):
        return "sd:-10:-10:-10\r\n"

    def calculateOneWheelVelocity(self,wheelAngle,angle,speed):
        velocity = int(speed * math.cos(math.radians(angle-wheelAngle)))
        return velocity

    def setSpeed(self,angle,speed):
        wheelOne = self.calculateOneWheelVelocity(self.wheelOneAngle,angle,speed)
        wheelTwo = self.calculateOneWheelVelocity(self.wheelTwoAngle,angle,speed)
        wheelThree = self.calculateOneWheelVelocity(self.wheelThreeAngle,angle,speed)

        setSpeedCommandString = "sd:" + str(wheelOne)+":"+str(wheelTwo)+":"+str(wheelThree) + "\r\n"

        return setSpeedCommandString

    def motorsOff(self):
        return "sd:0:0:0\r\n"

    def robotSpeedDiagonally(self,speedX,speedY):
        robotSpeed = math.sqrt(speedX * speedX + speedY * speedY)
        return robotSpeed

    def robotAngleDiagonally(self,speedX,speedY):
        robotDirectionAngle = math.atan2(speedY, speedX)
        return robotDirectionAngle





