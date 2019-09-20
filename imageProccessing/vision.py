import json

import cv2
from imageProccessing import configuration
import numpy as np
import pyrealsense2 as rs
import time


class vision:

    def __init__(self):
        conf = configuration.configuration()
        self.ball_color_range = conf.get("colors", conf.get("vision", "ball_color"))
        self.ball_noise_kernel = conf.get("vision", "ball_noise_kernel")
        self.blue_basket_color_range = conf.get("colors", conf.get("vision", "blue_basket_color"))
        self.magenta_basket_color_range = conf.get("colors", conf.get("vision", "magenta_basket_color"))

    def find_compatible_camera(self):
        ctx = rs.context()
        ds5_dev = rs.device()
        devices = ctx.query_devices();
        DS5_product_ids = ["0AD1", "0AD2", "0AD3", "0AD4", "0AD5", "0AF6", "0AFE", "0AFF", "0B00", "0B01", "0B03",
                           "0B07"]
        for dev in devices:
            if dev.supports(rs.camera_info.product_id) and str(
                    dev.get_info(rs.camera_info.product_id)) in DS5_product_ids:
                if dev.supports(rs.camera_info.name):
                    print("Found device that supports advanced mode:", dev.get_info(rs.camera_info.name))
                return dev
        raise Exception("No device that supports advanced mode was found")

    def configure_rs_camera(self):
        try:
            dev = self.find_compatible_camera()
            advnc_mode = rs.rs400_advanced_mode(dev)
            while not advnc_mode.is_enabled():
                advnc_mode.toggle_advanced_mode(True)
                time.sleep(5)
                # The 'dev' object will become invalid and we need to initialize it again
                dev = self.find_compatible_camera()
                advnc_mode = rs.rs400_advanced_mode(dev)

            """
           # To get the minimum and maximum value of each control use the mode value:
           query_min_values_mode = 1
           query_max_values_mode = 2

           current_std_depth_control_group = advnc_mode.get_depth_control()

           min_std_depth_control_group = advnc_mode.get_depth_control(query_min_values_mode)
           max_std_depth_control_group = advnc_mode.get_depth_control(query_max_values_mode)

           # Set some control with a new (median) value
           current_std_depth_control_group.scoreThreshA = int(
               (max_std_depth_control_group.scoreThreshA - min_std_depth_control_group.scoreThreshA) / 2)
           advnc_mode.set_depth_control(current_std_depth_control_group)

           # Serialize all controls to a Json string
           serialized_string = advnc_mode.serialize_json()
           print("Controls as JSON: \n", serialized_string)
           """

            with open('custompreset.json', 'r') as f:
                distros_dict = json.load(f)

            as_json_object = json.loads(str(distros_dict).replace("'", '\"'))

            # We can also load controls from a json string
            # The C++ JSON parser requires double-quotes for the json object so we need
            #  to replace the single quote of the pythonic json to double-quotes
            json_string = str(as_json_object).replace("'", '\"')
            advnc_mode.load_json(json_string)

        except Exception as e:
            print(e)
        pass

    def apply_ball_color_filter(self, hsv):
        # Apply ball color filter
        mask = cv2.inRange(hsv, self.ball_color_range["min"], self.ball_color_range["max"])
        kernel = np.ones((5, 5), np.uint8)
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        return opening

    def apply_basket_color_filter(self, hsv, color):
        # Apply ball color filter
        if (color == "blue"):
            mask = cv2.inRange(hsv, self.blue_basket_color_range["min"], self.blue_basket_color_range["max"])
            kernel = np.ones((5, 5), np.uint8)
            opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        elif (color == "magenta"):
            mask = cv2.inRange(hsv, self.magenta_basket_color_range["min"], self.magenta_basket_color_range["max"])
            kernel = np.ones((5, 5), np.uint8)
            opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        return opening

    def detect_ball(self, mask):
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
        return detector.detect(mask)

    def detect_basket(self, thresholded_image):

        contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        font = cv2.FONT_HERSHEY_COMPLEX

        for cnt in contours:

            if cv2.contourArea(cnt) > 300:
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                im = cv2.drawContours(thresholded_image, [box], 0, (100, 100, 255), 5)
                area = cv2.contourArea(cnt)
