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
        self.key = 0
        self.basketX = 0
        self.basketY = 0
        self.depth = 0
        self.ballX = 0
        self.ballY = 0

        self.gameStopped = False

    def get_basketX(self):
        return self.basketX

    def get_ballX(self):
        return self.ballX

    def get_ballY(self):
        return self.ballY

    def getDepth(self):
        return self.depth

    def getBasketDepth(self):
        return self.basket_depth

    def run(self):
        # Frame timer for FPS display
        fps = 0
        frame_counter = 0
        frame_counter_start = time.time()

        pipeline = rs.pipeline()
        config = rs.config()

        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.vision.configure_rs_camera()
        pipeline.start(config)

        while True:
            # Read BGR frame
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            # Convert to HSV

            hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
            blurred_image = cv2.medianBlur(hsv,5)

            ball_color_mask = self.vision.apply_ball_color_filter(blurred_image)
            blue_basket_mask = self.vision.apply_basket_color_filter(blurred_image, "blue")
            magenta_basket_mask = self.vision.apply_basket_color_filter(blurred_image, "magenta")


            # Depending on which side is the robot the correct mask is picked
            attack_blue_mask = cv2.bitwise_xor(blue_basket_mask, ball_color_mask)
            attack_magenta_mask = cv2.bitwise_or(magenta_basket_mask,
                                                 ball_color_mask)

            #ball_keypoints = self.vision.detect_ball(attack_blue_mask)
            self.basketX, self.basketY = self.vision.detect_basket(blue_basket_mask,attack_blue_mask)
            #self.basket_depth = depth_frame.get_distance(int(float(self.basketX)), int(float(self.basketY)))
            self.ballX, self.ballY = self.vision.detect_ball(ball_color_mask,attack_blue_mask)


            """
            for keypoint in ball_keypoints:
                self.ballX = keypoint.pt[0]
                self.ballY = keypoint.pt[1]
                ##self.ballSize = keypoint.pt[2]
                self.depth = depth_frame.get_distance(int(float(self.ballX)), int(float(self.ballY)))
                #shape = vision.detect_shape(color_image, attack_blue_mask)
                cv2.putText(color_image, str(round(self.depth, 3)) + " ball", (int(self.ballX), int(self.ballY)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 255, 255))
            im_with_keypoints = cv2.drawKeypoints(attack_blue_mask, ball_keypoints, np.array([]), (0, 0, 255),
                                                  cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            """
            # Handle keyboard input
            self.key = cv2.waitKey(1) & 0xFF

            if self.key == ord("q"):
                self.gameStopped = True
                break

            frame_counter += 1

            if frame_counter % 10 == 0:
                frame_counter_end = time.time()
                fps = int(10 / (frame_counter_end - frame_counter_start))
                frame_counter = 0
                frame_counter_start = time.time()

            cv2.putText(color_image, str(fps), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

            #cv2.imshow("frame", color_image)
            cv2.imshow("ball_color", attack_blue_mask)
        cv2.destroyAllWindows()