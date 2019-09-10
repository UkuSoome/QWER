import serial
import cv2
ser = serial.Serial('/dev/ttyUSB0')


ser.write("sd:10:10:0:0").encode("utf-8")


def motorsOff():
    ser.write("sd:0:0:0:0").encode("utf-8")

def driveForward():
    ser.write("sd:10:10:0:0").encode("utf-8")

def driveLeft():
    ser.write("sd:10:0:10:0").encode("utf-8")  ## test it

def driveRight():
    ser.write("sd:0:10:10:0").encode("utf-8") ## test it

def driveBackwards():
    ser.write("sd:-10:-10:0:0").encode("utf-8")
while (1):
    key = cv2.waitKey(1) & 0xFF
    if key == ord('w'):
        driveForward()
    if key == ord("s"):
        driveBackwards()
    if key == ord("a"):
        driveLeft()
    if key == ord("d"):
        driveRight()
    if key == ord('q'):
        motorsOff()
        break

motorsOff()
ser.close()