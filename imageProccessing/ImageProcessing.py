import cv2
import time
from imageProccessing import vision
from imageProccessing import configuration
import numpy as np
import pyrealsense2 as rs
from collections import deque
import math

class ImageProccessing:

    def __init__(self):

        ## muutujad
        self.conf = configuration.configuration()
        self.vision = vision.vision()
        self.key = 0
        self.basketX = 0
        self.basketY = 0
        self.basketDistance = 0
        self.ballX = 0
        self.ballY = 0
        self.ballDistance = 0
        self.blackAreaX = 0
        self.blackAreaY = 0
        self.gameStopped = False
        self.blueBasket = True
        self.gameState = True

    def setGameState(self,gameState):
        self.gameState = gameState

    def get_basketX(self):
        return self.basketX

    def get_basketY(self):
        return self.basketY

    def get_ballX(self):
        return self.ballX

    def get_ballY(self):
        return self.ballY

    def getBasketDistance(self):
        return self.basketDistance


    def getBallDistance(self):
        return self.ballDistance

    def run(self):
        # Frame timer for FPS display
        fps = 0
        frame_counter = 0
        frame_counter_start = time.time()

        pipeline = rs.pipeline()
        config = rs.config()

        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)
        self.vision.configure_rs_camera()
        pipeline.start(config)
        basketDistance = 0

        basket_distance_buffer = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ball_distance_buffer = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        kaamerakorgus = 0.232 # meetrites

        while True:

            # Read BGR frame
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            #depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            # Convert to HSV

            hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
            #qqqqqqkernel = np.ones((3,3), np.uint8)
            #closing = cv2.morphologyEx(hsv, cv2.MORPH_OPEN, kernel)
            #blurred_image = cv2.medianBlur(hsv,5)

            ball_color_mask = self.vision.apply_ball_color_filter(hsv)
            blue_basket_mask = self.vision.apply_basket_color_filter(hsv, "blue")
            magenta_basket_mask = self.vision.apply_basket_color_filter(hsv, "magenta")
            ##black_color_mask = self.vision.apply_black_filter(closing)


            # Depending on which side is the robot the correct mask is pickedqq
            if self.blueBasket:
                attack_blue_mask = cv2.bitwise_xor(blue_basket_mask, ball_color_mask)
                self.basketX, self.basketY = self.vision.detect_basket(blue_basket_mask, attack_blue_mask)
                self.ballX, self.ballY = self.vision.detect_ball(ball_color_mask, attack_blue_mask)
            else:
                attack_magenta_mask = cv2.bitwise_xor(magenta_basket_mask, ball_color_mask)
                self.basketX, self.basketY = self.vision.detect_basket(magenta_basket_mask, attack_magenta_mask)
                self.ballX, self.ballY = self.vision.detect_ball(ball_color_mask, attack_magenta_mask)

            #self.basketX, self.basketY = self.vision.detect_basket(magenta_basket_mask, attack_magenta_mask)
            #self.ballX, self.ballY = self.vision.detect_ball(ball_color_mask, attack_magenta_mask)
            """self.blackAreaX1, self.ballY1, self.blackAreaX2, self.ballY2 = self.vision.line_on_black(black_color_mask,
                                                                                                     attack_blue_mask)
            """
            if self.basketX != -1:
                basket_distance = depth_frame.get_distance(int(float(self.basketX)), int(float(self.basketY)))
                rounded_basket_distance = round(basket_distance,3)
                basket_distance_buffer.append(rounded_basket_distance)
                basket_distance_buffer.pop(0)
                self.basketDistance = self.vision.calculate_distance_with_buffer(basket_distance_buffer)

            if self.ballX != -1:
                ball_distance = depth_frame.get_distance(int(float(self.ballX)), int(float(self.ballY)))
                rounded_ball_distance = round(ball_distance, 3)
                ball_distance_buffer.append((rounded_ball_distance))
                ball_distance_buffer.pop(0)
                ballDistance = self.vision.calculate_distance_with_buffer(ball_distance_buffer)
                if ballDistance > kaamerakorgus:
                    self.ballDistance = math.sqrt(ballDistance**2 - kaamerakorgus**2)
                else:
                    self.ballDistance = -1

            if self.blueBasket:
                cv2.line(attack_blue_mask, (320, 0), (320, 480), (100, 255, 180), 2)
                cv2.line(attack_blue_mask, (0, 229), (640, 229), (100, 255, 180), 2)
            else:
                cv2.line(attack_magenta_mask, (320, 0), (320, 480), (100, 255, 180), 2)
                cv2.line(attack_magenta_mask, (0, 229), (640, 229), (100, 255, 180), 2)

            # Handle keyboard input
            self.key = cv2.waitKey(1) & 0xFF

            if self.key == ord("q"):
                self.gameStopped = True
                break
            if self.gameState == False:
                break
            frame_counter += 1

            if frame_counter % 10 == 0:
                frame_counter_end = time.time()
                fps = int(10 / (frame_counter_end - frame_counter_start))
                frame_counter = 0
                frame_counter_start = time.time()

            if self.basketX != -1:
                if self.blueBasket:
                    cv2.putText(attack_blue_mask, "BASKET DISTANCE: " + str(rounded_basket_distance), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (100, 255, 255))

                else:
                    cv2.putText(attack_magenta_mask, "BASKET DISTANCE: " + str(rounded_basket_distance), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (100, 255, 255))

            #if self.ballX != -1:
                #if self.blueBasket:
                    #cv2.putText(attack_magenta_mask, "BALL DISTANCE: " + str(rounded_ball_distance), (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (100, 255, 255))

                #else:
                    #cv2.putText(attack_magenta_mask, "BALL DISTANCE: " + str(rounded_ball_distance), (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (100, 255, 255))

            cv2.putText(attack_blue_mask, str(fps), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

            cv2.imshow("frame", color_image)
            if self.blueBasket:
                cv2.imshow("ball_color", attack_blue_mask)
            else:
                cv2.imshow("ball_color",  attack_magenta_mask)
        cv2.destroyAllWindows()