import serial
import cv2
import numpy as np
import math

ser = serial.Serial('/dev/ttyACM1')

wheelOneAngle = 60
wheelTwoAngle = 180
wheelThreeAngle = 300

def rotateLeft():
    return "sd:10:10:10\r\n"


def rotateRight():
    return "sd:-10:-10:-10\r\n"

def calculateOneWheelVelocity(wheelAngle,angle,speed):
    velocity = int(speed * math.cos(math.radians(angle - wheelAngle)))
    return velocity

def setSpeed(angle,speed):
    wheelOne = calculateOneWheelVelocity(wheelOneAngle,angle,speed)
    wheelTwo = calculateOneWheelVelocity(wheelTwoAngle,angle,speed)
    wheelThree = calculateOneWheelVelocity(wheelThreeAngle,angle,speed)

    setSpeedCommandString = "sd:" + str(wheelOne)+":"+str(wheelTwo)+":"+str(wheelThree) + "\r\n"

    return setSpeedCommandString

def motorsOff():
    return "sd:0:0:0\r\n"

frame = np.zeros((200,200))
cv2.imshow("frame",frame)
while 1:
    key = cv2.waitKey(0)
    print(key)
    if key == ord('w'):
        ser.write(setSpeed(0,10).encode("utf-8"))
    if key == ord("s"):
        ser.write(setSpeed(180,10).encode("utf-8"))
    if key == ord("a"):
        ser.write(setSpeed(90,10).encode("utf-8"))
    if key == ord("d"):
        ser.write(setSpeed(270,10).encode("utf-8"))
    if key == ord("c"):
        ser.write(rotateLeft().encode("utf-8"))
    if key == ord("v"):
       ser.write(rotateRight().encode("utf-8"))
    if key == ord('q'):
        ser.write('sd:0:0:0\r\n'.encode('utf-8'))
        cv2.destroyAllWindows()
        ser.close()
        break
cv2.destroyAllWindows()
ser.write('sd:0:0:0\r\n'.encode('utf-8'))
ser.close()