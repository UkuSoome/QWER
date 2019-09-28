import serial
import time

class MainboardCommunication:

    def __init__(self,port):
        self.ser = serial.Serial(port)

    def readBytes(self):
        if self.ser.in_waiting:
            line = self.ser.readline().decode("ascii")
            return line.split(":")
        return []

    def waitForAnswer(self):
        msg = self.readBytes()
        starttime = time.time()
        while time.time() - starttime < 5:
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