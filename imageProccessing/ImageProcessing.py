import cv2
import time
from imageProccessing import vision
from imageProccessing import configuration
import numpy as np
import pyrealsense2 as rs

class ImageProccessing:

    def __init__(self):

        ## muutujad

        self.conf = configuration.configuration()
        self.vision = vision.vision()
        self.attackBlueMask = np.zeros((5, 5))
        self.depth = 0

    def getBallMask(self):
        return self.attackBlueMask

    def getDepth(self):
        return self.depth

    def run(self):
        # Capture camera
        #device = self.conf.get("vision", "video_capture_device")
        #cap = cv2.VideoCapture(device)

        # Frame timer for FPS display
        fps = 0
        frame_counter = 0
        frame_counter_start = time.time()

        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        profile = pipeline.start(config) ####  THIS IS UNUSED; WHAT DOES IT DOE FRED?!??!
        while True:
            # Read BGR frame
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            depth_image = np.asanyarray(depth_frame.get_data()) ###  THIS IS UNUSED; WHAT DOES IT DOE FRED?!??!
            color_image = np.asanyarray(color_frame.get_data())
            print(color_image.size)

            # Convert to HSV

            hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

            ball_color_mask = self.vision.apply_ball_color_filter(hsv)
            blue_basket_mask = self.vision.apply_basket_color_filter(hsv, "blue")
            magenta_basket_mask = self.vision.apply_basket_color_filter(hsv, "magenta")

            # Depending on which side is the robot the correct mask is picked
            self.attack_blue_mask = cv2.bitwise_or(blue_basket_mask, ball_color_mask)
            attack_magenta_mask = cv2.bitwise_or(magenta_basket_mask, ball_color_mask) ### THIS IS UNUSED; WHAT DOES IT DOE FRED?!??!


            ###ball_detector = self.vision.detect_ball(attack_blue_mask) ## this might be needed later

            """keypoints = detector.detect(attack_blue_mask)"""
            ball_keypoints = self.vision.detect_ball(self.attack_blue_mask)

            for keypoint in ball_keypoints:
                x, y = keypoint.pt
                self.depth = depth_frame.get_distance(int(float(x)), int(float(y)))
                """shape = vision.detect_shape(color_image, attack_blue_mask)"""
                cv2.putText(color_image, str(round(self.depth, 3)) + " ball", (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 255, 255))
            im_with_keypoints = cv2.drawKeypoints(self.attack_blue_mask, ball_keypoints, np.array([]), (0, 0, 255),
                                                  cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            # Handle keyboard input
            key = cv2.waitKey(1)

            if key & 0xFF == ord("q"):
                break

            # FPS display
            frame_counter += 1

            if frame_counter % 10 == 0:
                frame_counter_end = time.time()
                fps = int(10 / (frame_counter_end - frame_counter_start))
                frame_counter = 0
                frame_counter_start = time.time()

            cv2.putText(color_image, str(fps), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

            # Show frame
            cv2.imshow("frame", color_image)
            cv2.imshow("ball_color", im_with_keypoints)

        # Exit cleanly
       # cap.release()
        cv2.destroyAllWindows()
