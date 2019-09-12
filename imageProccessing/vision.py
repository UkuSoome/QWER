import cv2
from imageProccessing import configuration
import numpy as np



# Get color ranges and noise removal kernels from config


# Get boolean image with ball color filter applied
class vision:

    def __init__(self):
        conf = configuration.configuration()
        self.ball_color_range = conf.get("colors", conf.get("vision", "ball_color"))
        self.ball_noise_kernel = conf.get("vision", "ball_noise_kernel")
        self.blue_basket_color_range = conf.get("colors", conf.get("vision", "blue_basket_color"))
        self.magenta_basket_color_range = conf.get("colors", conf.get("vision", "magenta_basket_color"))


    def apply_ball_color_filter(self,hsv):
        # Apply ball color filter
        mask = cv2.inRange(hsv, self.ball_color_range["min"], self.ball_color_range["max"])
        kernel = np.ones((5, 5), np.uint8)
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        return opening

    def apply_basket_color_filter(self,hsv, color):
        # Apply ball color filter
        if(color == "blue"):
            mask = cv2.inRange(hsv, self.blue_basket_color_range["min"], self.blue_basket_color_range["max"])
            kernel = np.ones((5, 5), np.uint8)
            opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        elif(color == "magenta"):
            mask = cv2.inRange(hsv, self.magenta_basket_color_range["min"], self.magenta_basket_color_range["max"])
            kernel = np.ones((5, 5), np.uint8)
            opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        return opening

    def detect_ball(self,thresholded_image):
        # Setup SimpleBlobDetector parameters.
        params = cv2.SimpleBlobDetector_Params()
        params.filterByColor = True
        params.blobColor = 255
        # Filter by Area.
        params.filterByArea = True
        params.minArea = 70

        # Filter by Circularity
        params.filterByCircularity = True
        params.minCircularity = 0.1

        # Filter by Convexity
        params.filterByConvexity = True
        params.minConvexity = 0.87

        # Filter by Inertia
        params.filterByInertia = True
        params.minInertiaRatio = 0.75

        # Create a detector with the parameters
        ver = (cv2.__version__).split('.')
        if int(ver[0]) < 3:
            detector = cv2.SimpleBlobDetector(params)
        else:
            detector = cv2.SimpleBlobDetector_create(params)
        return detector