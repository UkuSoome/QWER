import serial
import time

class MainboardCommunication:

    def __init__(self,port,imgHandler):
        self.ser = serial.Serial(port)
        self.imgHandler = imgHandler
        self.motorSpeeds = ""
        self.throwerSpeed = ""

    def setMotorSpeeds(self,msg):
        self.motorSpeeds = msg
    def setThrowerSpeed(self,msg):
        self.throwerSpeed = msg
    def readBytes(self):
        if self.ser.in_waiting:
            line = self.ser.readline().decode("ascii").rstrip()
            self.ser.flush()
            return line.split(":")
        return []

    def waitForAnswer(self):
        msg = self.readBytes()
        starttime = time.time()
        while time.time() - starttime < 2:
            if len(msg) > 0:
                return msg
            msg = self.readBytes()
        print("Mainboard crashed.")
        return msg

    def sendBytes(self, msg):
        msg += "\r\n"
        self.ser.write(msg.encode("utf-8"))

    def closeSerial(self):
        self.ser.close()

    # def run(self):
    #     self.sendBytes('d:125')
    #     while True:
    #         if self.motorSpeeds != "":
    #             self.sendBytes(self.motorSpeeds)
    #             self.waitForAnswer()
    #             self.motorSpeeds = ""
    #         if self.throwerSpeed != "":
    #             self.sendBytes(self.throwerSpeed)
    #             self.throwerSpeed = ""
    #         if self.imgHandler.gameStopped:
    #             self.sendBytes("sd:0:0:0")
    #             self.waitForAnswer()
    #             break
    #     self.closeSerial()