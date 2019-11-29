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
        self.BOB2 = 0
        self.ballDistance = 0
        self.gameState = True
        self.refHandler = RefHandler.RefHandler('C', 'C',mainComm)
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
            0.7967:149,
            0.8392:149, ## töötab
            0.8439:149,
            0.8618:150, ## töötab
            0.86795: 150,
            0.8702:150, ## töötab
            0.8752:150,
            0.88275: 150,
            0.88505: 150, ## töötab
            0.88615:150,
            0.8863:150,
            0.8924:151,
            0.9227:151,
            0.9317:151, ## töötab
            0.9387:152,
            0.9703:152,
            1.01435:152,
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
            1.26805:156,
            1.30755:156,
            1.3305:156, ## töötab
            1.34665:156,
            1.3553:156,
            1.36025:156, ## töötab
            1.36815:156,
            1.3708:157, ## töötab
            1.37835:157,
            1.38145:157, ## töötab
            1.38185:157, ## töötab
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
            1.4994:158,
            1.49035:159, ## töötab
            1.52375:159,
            1.53105:159,##töötab
            1.56035:159, ## töötab
            1.5652:159,
            1.56695:159, ## töötab
            1.58195:160,
            1.6179:160,
            1.64115:160, ## töötab
            1.67515:160,
            1.68015:160, ## töötab
            1.71955:160,
            1.72915:161, ## töötab
            1.73215:161,
            1.7351:161, #töötab
            1.8141:161, ## töötab
            1.8184:161, ## töötab
            1.83145:161,## töötab
            1.84425:161, ## töötab
            1.8774:162,
            1.90965:162,
            1.92405:163,
            1.9536:164,
            2.05755:164,
            2.1055:164,
            2.12375:164, ## töötab
            2.1297:165,
            2.16765:165,
            2.29265:166, ## töötab
            2.2968:166,
            2.30665:166, ## töötab
            2.31655:166,
            2.32205:167,
            2.3522:167, ## töötab
            2.3523:167, ## töötab
            2.3583:167,
            2.36505:167, ## töötab
            2.37525:167,
            2.3974:167,
            2.43155:167,
            2.46395:167, ## töötab
            2.47575:168,
            2.52345:168, ## töötab
            2.5298:168,
            2.54115:169, ## töötab
            2.5513:169, ## töötab
            2.568988:169,
            2.5754:169, ## töötab
            2.59505:169, ## töötab
            2.65405:169,
            2.65475:169, ## töötab
            2.6687:169,
            2.6977:170,
            2.7123:171,
            2.74865:172, ## töötab
            2.7624:172,
            2.8025:172,##töötab
            2.8151:172,
            2.8207:172,
            2.8534:173,
            2.8684:174,
            3.0447:174,
            3.0864:174,
            3.11415:175,
            3.22085:175,
            3.25145:175, ## töötab
            3.29015:178, ## töötab
            3.30775:178, ## töötab
            3.3351:178,
            3.3493:181,
            3.4432:182,
            3.5946:183,## töötab
            3.66665:183,
            3.82695:184,
            3.83605:184,
            3.86745:184, ## töötab
            3.89205:184,
            3.92335:184, ## töötab
            3.96405:185,
            3.9832:185,
            4.04305:186, ## töötab
            4.0443:186,
            4.04895:187,
            4.05395:187, ## töötab
            4.0665:188,
            4.11135:189,
            4.1234:189,
            4.12375:189, ## töötab
            4.14:190,
            4.14645:192,
            4.1532:194,
            4.25175:194,
            4.26385:195,
            4.278:196,
            4.31475:196,
            4.3265:196, ## töötab
            4.32675:196, ## töötab
            4.3518:198,
            4.42505:198,
            4.3589:198, ## töötab
            4.45995:200,
            4.4823:206,
            4.49455:207,
            4.51355:208,
            4.52085:209,
            4.5228:209, ## töötab
            4.53175:211,
            4.5355:212, ## töötab
            4.5455:213,
            4.56765:214, ## töötab
            4.5683:214,
            4.57415:215,
            4.618:215,
            4.63355:215,
            4.66335:217,
            4.66655:218,
            4.6735:219,
            4.7085:219,
            4.70914:219,
            4.7116:220,
            4.7313:221,
            4.7522:221, ## töötab
            4.8036:224,
            4.84225:244,
            4.8505:246,
            4.8554:246,
            4.8639:246,
            4.87105:247,
            4.8787:249,
            4.88135:250,
            4.9252:250,
            4.998:250,
            5.022:250,
            5.0983:250,
            5.12575:250, ## töötab
            5.1757:250,
        }
    def run(self):
        time.sleep(2)
        reftime = time.time()
        while 1:
            if self.gameState:
                if self.BOB > 1600:
                    self.BOB = 0
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
                """if time.time() - reftime > 0.1:
                    msg = self.mainComm.readBytes()
                    if len(msg) > 0:
                        if msg != None:
                            command = msg[0]
                            print(msg)
                            if command == "<ref":
                                cmd = self.refHandler.handleMsg(msg[1])
                                print(cmd)
                                if cmd == "STOP":
                                    self.imgHandler.setGameState(False)
                                    self.mainComm.waitForAnswer()
                                    self.mainComm.sendBytes(self.wheelLogic.motorsOff())
                                    self.mainComm.waitForAnswer()
                                    self.mainComm.closeSerial()
                                    break"""
            else:
                self.readMb()

            if self.imgHandler.gameStopped:
                self.mainComm.waitForAnswer()
                self.mainComm.sendBytes(self.wheelLogic.motorsOff())
                self.mainComm.waitForAnswer()
                self.mainComm.closeSerial()
                break
    def setGameState(self,gameState):
        self.gameState = gameState
    def adjustDistance(self):
        self.ballDistance = self.imgHandler.getBallDistance()
        if 0.26 <= self.ballDistance <= 0.3:
            print("palli kaugus")
            self.mainComm.sendBytes(self.wheelLogic.motorsOff())
            self.mainComm.waitForAnswer()
            self.ballDistanced = True
            timenow = time.time()
            while time.time() - timenow < 0.15:
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
                if self.BOB >= 1500:
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
            self.BOB += 1
            if self.BOB >= 1500:
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
        speed = 0.14
        if self.basketY != -1:
            if 210 <= self.basketY <= 250:
                speed = 0.04
            elif 170 <= self.basketY <= 290:
                speed = 0.09
            elif 50 <= self.basketY <= 430:
                speed = 0.12
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
        if self.ballX >= 320:
            self.BOB = 0
            print("jõudsin pallini")
            #self.mainComm.setMotorSpeeds(self.wheelLogic.motorsOff())
            self.mainComm.sendBytes(self.wheelLogic.motorsOff())
            self.mainComm.waitForAnswer()
            self.ballReached = True
            if self.BOB == 0:
                time.sleep(0.1)

            return
        self.ballY = self.imgHandler.get_ballY()
        speed = 0.24
        self.ballX = self.imgHandler.get_ballX()
        if self.BOB < 10:
            speed = 0.12
        if self.ballX >= 260:
            speed = 0.12
        if self.ballY != -1:
            if self.BOB > 500:
                self.mainComm.sendBytes(self.wheelLogic.motorsOff())
                self.mainComm.waitForAnswer()
                self.ballFound = False
                self.BOB = 0
                return
        else:
            self.BOB = 0
        if self.ballY<= self.screenMidPointY:
            #self.mainComm.setMotorSpeeds(self.wheelLogic.setSpeed(90 + angle,0,0.07))
            self.mainComm.sendBytes(self.wheelLogic.setSpeed(90 + angle,0,speed))
            self.mainComm.waitForAnswer()
        elif self.ballY >= self.screenMidPointY:
            #self.mainComm.setMotorSpeeds(self.wheelLogic.setSpeed(90 - angle,0,0.07))
            self.mainComm.sendBytes(self.wheelLogic.setSpeed(90 - angle,0,speed))
            self.mainComm.waitForAnswer()
        self.BOB += 1


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
            self.mainComm.sendBytes(self.wheelLogic.motorsOff())
            self.mainComm.waitForAnswer()
            if self.BOB2 > 30:
                if self.basketY != -1:
                    self.basketCentered = True
                self.BOB2 = 0
            else:
                self.ballCentred = False
            self.BOB2 +=1
            return
        speed = 0.07
        self.basketY = self.imgHandler.get_basketY()
        if self.basketY != -1:
            if 180 <= self.basketY <= 260:
                speed = 0.015
            elif 120 <= self.basketY <= 320:
                speed = 0.020
            elif 80 <= self.basketY <= 430:
                speed = 0.045
            if 0 <= self.basketY < self.screenMidPointY+20:
                #self.mainComm.setMotorSpeeds(self.wheelLogic.setSpeed(0,omega,0.03))
                self.mainComm.sendBytes(self.wheelLogic.setSpeed(0, omega, speed))
            elif self.screenMidPointY +30 <= self.basketY <= 480:
                #self.mainComm.setMotorSpeeds(self.wheelLogic.setSpeed(0,omega,0.03))
                self.mainComm.sendBytes(self.wheelLogic.setSpeed(180, -omega, speed))
        else:
            #self.mainComm.setMotorSpeeds(self.wheelLogic.setSpeed(0,omega,0.03))
            self.mainComm.sendBytes(self.wheelLogic.setSpeed(0, omega, 0.09))
        self.mainComm.waitForAnswer()
        if self.BOB == 250:
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
                    self.gameState = True
                elif cmd == "STOP":
                    self.gameState = False
                    return
                elif cmd == "PING":
                    print("Sending ACK")

    def readMb(self):
        mbMsg = self.mainComm.readBytes()
        if len(mbMsg) > 0:
            self.handleMbCommands(mbMsg)









