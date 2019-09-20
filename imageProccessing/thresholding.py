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
    # Try to get saved range from config file, use whole color space as default if not saved
    # Color ranges are saved as { "min": (hmin, smin, vmin), "max": (hmax, smax, vmax) }
    color_range = conf.get("colors", color_name, default={"min": (0, 0, 0), "max": (179, 255, 255)})
    mainComm = MainboardCommunication.MainboardCommunication()
    wheelLogic = WheelMovementLogic.WheelMovementLogic()
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

    # Capture camera
    ##device = conf.get("vision", "video_capture_device")
    ##cap = cv2.VideoCapture(device)

    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    vis.configure_rs_camera()
    pipeline.start(config)

    ##while cap.isOpened():
    while True:
        # Read BGR frame
        ##_, bgr = cap.read()
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        # Convert to HSV

        hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

        # TODO: also apply all the filters you do when actually running the robot (eg noise removal)
        # Apply color mask to HSV image
        mask = cv2.inRange(hsv, color_range["min"], color_range["max"])

        # Display filtered image
        cv2.imshow("frame", cv2.bitwise_and(color_image, color_image, mask=mask))

        # Handle keyboard input
        key = cv2.waitKey(1)

        if key & 0xFF == ord("q"):
            mainComm.sendBytes(wheelLogic.motorsOff())
            mainComm.waitForAnswer()
            mainComm.closeSerial()
            break
        if key == ord('w'):
            print(key)
            mainComm.sendBytes(wheelLogic.setSpeed(90, -10))
            mainComm.waitForAnswer()
        if key == ord("s"):
            mainComm.sendBytes(wheelLogic.setSpeed(270, -10))
            mainComm.waitForAnswer()
        if key == ord("a"):
            mainComm.sendBytes(wheelLogic.setSpeed(180, -10))
            mainComm.waitForAnswer()
        if key == ord("d"):
            mainComm.sendBytes(wheelLogic.setSpeed(0, -10))
            mainComm.waitForAnswer()
        if key == ord("c"):
            mainComm.sendBytes(wheelLogic.rotateLeft(10))
            mainComm.waitForAnswer()
        if key == ord("v"):
            mainComm.sendBytes(wheelLogic.rotateRight(10))

    # Overwrite color range
    conf.set("colors", color_name, color_range)
    conf.save()

    # Exit cleanly
    ##cap.release()
    ##cv2.destroyAllWindows()


if __name__ == "__main__":
    Tresh()