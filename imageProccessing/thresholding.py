import cv2
from functools import partial
from imageProccessing import vision
from imageProccessing import configuration
from mainboardCommunication import MainboardCommunication
from wheelMovementLogic import WheelMovementLogic
import numpy as np
import pyrealsense2 as rs


def Tresh():
    # Ask for color name to threshold
    color_name = input("Enter color name: ")
    conf = configuration.configuration()
    vis = vision.vision()
    color_range = conf.get("colors", color_name, default={"min": (0, 0, 0), "max": (179, 255, 255)})
    #mainComm = MainboardCommunication.MainboardCommunication('/dev/ttyACM0')
#    wheelLogic = WheelMovementLogic.WheelMovementLogic()
    # Create trackbars (sliders) for HSV channels
    cv2.namedWindow("frame")

    def update_range(i, j, value):
        values = list(color_range[i])
        values[j] = value
        color_range[i] = tuple(values)

    cv2.createTrackbar("h_min", "frame", color_range["min"][0], 179, partial(update_range, "min", 0))
    cv2.createTrackbar("s_min", "frame", color_range["min"][1], 255, partial(update_range, "min", 1))
    cv2.createTrackbar("v_min", "frame", color_range["min"][2], 255, partial(update_range, "min", 2))
    cv2.createTrackbar("h_max", "frame", color_range["max"][0], 179, partial(update_range, "max", 0))
    cv2.createTrackbar("s_max", "frame", color_range["max"][1], 255, partial(update_range, "max", 1))
    cv2.createTrackbar("v_max", "frame", color_range["max"][2], 255, partial(update_range, "max", 2))

    pipeline = rs.pipeline()
    config = rs.config()
    vis.configure_rs_camera()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)
    pipeline.start(config)

    while True:
        # Read BGR frame
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        # Convert to HSV

        hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
        # Apply color mask to HSV image
        mask = cv2.inRange(hsv, color_range["min"], color_range["max"])

        # Display filtered image
        cv2.imshow("frame", cv2.bitwise_and(color_image, color_image, mask=mask))

        # Handle keyboard input
        key = cv2.waitKey(1)

        if key & 0xFF == ord("q"):
            #mainComm.sendBytes(wheelLogic.motorsOff())
            #mainComm.waitForAnswer()
            #mainComm.closeSerial()
            break
        """
        if key == ord('w'):
            print(key)
            mainComm.sendBytes(wheelLogic.setSpeed(90, -100))
            mainComm.waitForAnswer()
        if key == ord("s"):
            mainComm.sendBytes(wheelLogic.setSpeed(270, -100))
            mainComm.waitForAnswer()
        if key == ord("a"):
            mainComm.sendBytes(wheelLogic.setSpeed(180, -100))
            mainComm.waitForAnswer()
        if key == ord("d"):
            mainComm.sendBytes(wheelLogic.setSpeed(0, -100))
            mainComm.waitForAnswer()
        if key == ord("c"):
            mainComm.sendBytes(wheelLogic.rotateLeft(20))
            mainComm.waitForAnswer()
        if key == ord("v"):
            mainComm.sendBytes(wheelLogic.rotateRight(20))
            mainComm.waitForAnswer()
        if key == ord('n'):
            mainComm.sendBytes("sd:15:0:0")
            mainComm.waitForAnswer()
        """
    # Overwrite color range
    conf.set("colors", color_name, color_range)
    conf.save()

if __name__ == "__main__":
    Tresh()