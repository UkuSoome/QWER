import math



class WheelMovementLogic:


    def __init__(self):

        self.wheelOneAngle = 0 ## this should be 0
        self.wheelTwoAngle = 120
        self.wheelThreeAngle = 240 ## this should be 240
        self.wheelDistanceFromCentre = 0.105
        self.wheelSpeedToMainboardUnits = 18.75 * 64 / (2 * math.pi * 0.035 * 60)

    def rotateLeft(self,speed):
        speedString = str(-speed)
        return "sd:" + speedString + ":" + speedString + ":" + speedString

    def rotateRight(self,speed):
        speedString = str(speed)
        return "sd:" + speedString + ":" + speedString + ":" + speedString

    def calculateOneWheelVelocity(self,wheelAngle,angle,speed,omega):
        velocity = int((speed * math.cos(math.radians(angle-wheelAngle))) + self.wheelDistanceFromCentre * omega)
        return velocity
    def calculateOmega(self,ballY):
        omega = (2*math.pi)/(((2*math.pi)*ballY)/2)
        return omega
    def setSpeed(self,angle,omega,speedLimit):
        wheelOne = int(round(speedLimit*self.wheelSpeedToMainboardUnits * (self.calculateOneWheelVelocity(self.wheelOneAngle,angle,10,omega))))
        wheelTwo = int(round(speedLimit*self.wheelSpeedToMainboardUnits * (self.calculateOneWheelVelocity(self.wheelTwoAngle,angle,10,omega))))
        wheelThree = int(round(speedLimit*self.wheelSpeedToMainboardUnits * (self.calculateOneWheelVelocity(self.wheelThreeAngle,angle,10,omega))))

        setSpeedCommandString = "sd:" + str(wheelOne)+":"+str(wheelTwo)+":"+str(wheelThree)

        return setSpeedCommandString

    def motorsOff(self):
        return "sd:0:0:0"

    def robotSpeedDiagonally(self,speedX,speedY):
        robotSpeed = math.sqrt(speedX * speedX + speedY * speedY)
        return robotSpeed

    def robotAngleDiagonally(self,speedX,speedY):
        robotDirectionAngle = math.atan2(speedY, speedX)
        return robotDirectionAngle

    def rotateLeftWithBackWheel(self,speed):
        return "sd:" + str(speed) + ":0:0"
    def rotateRightWithBackWheel(self,speed):
        return "sd:-" + str(speed) + ":0:0"


