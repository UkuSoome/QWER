from wheelMovementLogic import WheelMovementLogic

import serial
import cv2
import numpy as np
ser = serial.Serial('/dev/ttyACM0')




frame = np.zeros((200,200))
cv2.imshow("frame",frame)
wheelLogic = WheelMovementLogic.WheelMovementLogic()
while 1:
    key = cv2.waitKey(0) & 0xff
    print(key)
    if key == ord('w'):
        ser.write(wheelLogic.setSpeed(90,-10).encode("utf-8"))
    if key == ord("s"):
        ser.write(wheelLogic.setSpeed(270,-10).encode("utf-8"))
    if key == ord("a"):
        ser.write(wheelLogic.setSpeed(180,-10).encode("utf-8"))
    if key == ord("d"):
        ser.write(wheelLogic.setSpeed(0,-10).encode("utf-8"))
    if key == ord("c"):
        ser.write(wheelLogic.rotateLeft().encode("utf-8"))
    if key == ord("v"):
       ser.write(wheelLogic.rotateRight().encode("utf-8"))
    if key == ord("b"):
        ser.write("sd:0:0:10\r\n".encode("utf-8"))
    if key == ord('q'):
        ser.write('sd:0:0:0\r\n'.encode('utf-8'))
        cv2.destroyAllWindows()
        ser.close()
        break
cv2.destroyAllWindows()
ser.write('sd:0:0:0\r\n'.encode('utf-8'))
ser.close()
