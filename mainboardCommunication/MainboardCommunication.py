
import serial

class MainboardCommunication:

    def __init__(self):
        ## muutujad

        self.ser = serial.Serial('/dev/ttyACM0')

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