from wheelMovementLogic import WheelMovementLogic
from refHandler import RefHandler
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
            0.5059:145, ## töötab
            0.52835: 145, ## töötab
            0.65874:145,
            0.66035: 146,
            0.68074:146,
            0.68165:147,
            0.6977:147,
            0.71710: 147,
            0.7186:147,
            0.751:147,
            0.75265:148, ## töötab
            0.78285:148,
            0.82704:148,
            0.82775:149,
            0.8312:149, ## töötab
            0.8439:149,
            0.8618:150, ## töötab
            0.86795: 150,
            0.8702:150, ## töötab
            0.8752:150,
            0.88275: 150,
            0.88505: 150, ## töötab
            0.88615:150,
            0.8863:150,
            0.902:150,
            0.92115:150,
            0.9227:151,
            0.9317:151, ## töötab
            0.94635:151,
            0.95825:151,
            0.9504:151,
            0.965:151,
            0.97565:151,
            0.97895:151,
            0.9813:151,
            0.98645:151,
            0.9865:151,
            1.02085:151,
            1.0246:152, ## töötab
            1.04305:152,
            1.06484:152,
            1.0713:153,
            1.07945:153, ## töötab
            1.08:154,
            1.11965:154, ## töötab
            1.17175:154, ## Töötab
            1.19719:154,
            1.20135:154, ## töötab
            1.20965:155,
            1.22715:155, ## töötab
            1.2275:155,
            1.23125:155, ## töötab
            1.26545:155, ## töötab
            1.27925:155, ## töötab
            1.2834:155,
            1.30755:156,
            1.3305:156, ## töötab
            1.34665:156,
            1.35425:157,
            1.36235:157,
            1.3708:157, ## töötab
            1.37835:157,
            1.38145:157, ## töötab
            1.3823:157,
            1.40085:157,
            1.4047:157,
            1.40494:157,
            1.4061:157, ## töötab
            1.42325:157,
            1.4235:158,
            1.44035:158, ## töötab
            1.443:158, ## töötab
            1.44955:158,
            1.4547:158, ## töötab
            1.4894:158,
            1.49035:159, ## töötab
            1.50325:158,
            1.5112:158,
            1.5214:158,
            1.55925:158,
            1.5652:159,
            1.56695:159, ## töötab
            1.6041:159,
            1.61165:159,
            1.6179:160,
            1.67515:160,
            1.68015:160, ## töötab
            1.73215:161,
            1.8141:161, ## töötab
            1.8934:161,
            1.90965:162,
            1.96525:163,
            2.03905:163,
            2.06544:163,
            2.0785:163,
            2.0812:163,
            2.1055:164,
            2.16035:165,
            2.17475:165,
            2.2474:166,
            2.252:167,
            2.3444:167,
            2.4166:169,
            2.4374:170,
            2.48670:171,
            2.49354:173,
            2.5123:176,
            2.54025:176,
            2.63325:176,
            2.73485:176,
            2.7436:178,
            2.78345:179,
            2.7995:179,
            2.95425:180,
            2.98525:182,
            3.4512: 184,
            3.58795: 184,
            3.65775: 185,
            4.0525:189,
            4.0837: 191,
            4.12295: 192,
            4.1653:195,
            4.2365: 195,
            4.2636:198,
            4.30895: 198,
            4.35335:203,
            4.38740:203,
            4.4048:206,
            4.502:212,
            4.6108:213,
            4.686049999999991:217,
            4.71055:218,
            4.8038:218,
            4.79515:223,
            4.9368:227,
            5.24445:237,
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
        if 0.26 <= self.ballDistance <= 0.3:
            print("palli kaugus")
            self.mainComm.sendBytes(self.wheelLogic.motorsOff())
            self.mainComm.waitForAnswer()
            self.ballDistanced = True
            timenow = time.time()
            while time.time() - timenow < 0.3:
                self.mainComm.sendBytes(self.wheelLogic.motorsOff())
                self.mainComm.waitForAnswer()
            return
        self.ballDistance = self.imgHandler.getBallDistance()
        if -1 <= self.ballDistance < 0.26:
            self.ballDistance = self.imgHandler.getBallDistance()
            self.mainComm.sendBytes(self.wheelLogic.setSpeed(270,0,0.014))
            self.mainComm.waitForAnswer()
            if self.ballDistance == -1:
                self.BOB += 1
                if self.BOB >= 800:
                    self.ballFound = False
                    self.ballReached = False
                    self.ballCentred = False
                    self.BOB = 0
            else:
                self.BOB = 0
        elif 0.3 < self.ballDistance <= 3:
            self.ballDistance = self.imgHandler.getBallDistance()
            self.mainComm.sendBytes(self.wheelLogic.setSpeed(90,0,0.015))
            self.mainComm.waitForAnswer()
            if self.ballDistance == -1:
                self.BOB += 1
                if self.BOB >= 800:
                    self.ballFound = False
                    self.ballReached = False
                    self.ballCentred = False
                    self.BOB = 0

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
        if self.screenMidPointY+20 <= self.basketY <= self.screenMidPointY + 30:
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
            if 0 <= self.basketY < self.screenMidPointY+20:
                #self.mainComm.setMotorSpeeds(self.wheelLogic.setSpeed(0,omega,0.03))
                self.mainComm.sendBytes(self.wheelLogic.setSpeed(0, omega, speed))
            elif self.screenMidPointY +30 <= self.basketY <= 480:
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
        throwerSpeed = self.kaugused.get(basketDistance, self.kaugused[min(self.kaugused.keys(), key=lambda k: abs(k - basketDistance))])
        print(throwerSpeed)
        print(basketDistance)
        starttime = time.time()
        while time.time() - starttime <= 2.5:
            angle = self.calculateAngleToBasket(30)
            self.mainComm.sendBytes('d:'+str(int(throwerSpeed)))
            if self.basketY <= self.screenMidPointY+40:
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









