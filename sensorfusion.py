#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import the simple GoPiGo3 module
import easygopigo3 as go
import time
import signal
import sys
import serial
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import json
import cv2
import _thread
import scipy.stats as stats

# Update this variable every time you move to the next task
CURRENT_LAB09_TASK = 4.4
lastpos_us_ma = 1
lasttime_us_ma = 1
lastpos_us = 1
lasttime_us = 1
lastpos_cam = 1
lasttime_cam = 1
lastpos_enc = 1
lasttime_enc = 1
lastpos_comp = 1
lasttime_comp = 1
lastpos_kalman = 1
lasttime_kalman = 1
# Retrieve data from ultrasonic sensor and line following module connected to Arduino
def getDataFromArduino(ser):
    data = []
    ser.write("R".encode()) # Request data

    # Read and parse the serial buffer
    while ser.in_waiting > 0:
        serial_line = ser.readline().strip()
        try:
            data = json.loads(serial_line.decode())
        except Exception as e:
            print(e)
    return data


def fastWorker():
    global running, ser, arduino_data, us_pos, enc_pos, cam_pos
    print("Starting fastWorker in a separate thread")

    #Create an instance of the robot with a constructor from the easygopigo3 module that was imported as "go".
    robot = go.EasyGoPiGo3()

    # Set speed for the GoPiGo robot in degrees per second
    robot.set_speed(60)
    robot.reset_encoders()

    # Distance from the START marker to the wall in mm
    start_to_wall_dist = 1300 

    # Initialize serial
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)

    while running:
        # Get the readings of ultrasonic and line following sensor
        # and store them to arduino_data global variable
        arduino_data = getDataFromArduino(ser) 
        #print(arduino_data)

        ##########################################################
        # Task 4: Get the averaged encoder value and use it to   #
        #         find the distance from the wall in millimeters #
        ##########################################################
        enc_pos = start_to_wall_dist - robot.read_encoders_average(units='cm')*10

        if arduino_data:
            ls1 = arduino_data['ls1']
            ls2 = arduino_data['ls2']
            ls3 = arduino_data['ls3']
            ls4 = arduino_data['ls4']
            ls5 = arduino_data['ls5']
            clp = arduino_data['clp']
            near = arduino_data['near']
            us_pos = arduino_data['us1']

            ############################################################
            # Copy your line following and marker detection logic here #
            ############################################################
            if clp == 1 or near == 1:
                robot.stop()

            elif ls5 == 0:
                robot.right()

            elif ls3 == 0:
                robot.left()

            else:
                robot.forward()

            #                                                          #
            #                                                          #
            #                                                          #
            #                                                          #
            #################################################
        else:
            print("No data received from Arduino!")

        time.sleep(0.02) # Limit control thread to 50 Hz

    # Stop the robot when not running any more
    print("STOPPING fastWorker")
    robot.stop()
    sys.exit(0)

posarray = np.zeros(20)
for i in range(20):
    posarray = np.append(posarray,1700)
# Moving average filter
def movingAverage(pos):
    ####################################################
    # Lab 09 Task 2: Implement moving average filter.  #
    ####################################################
    global posarray
    posarray = np.append(posarray,pos)
    posarray = np.delete(posarray,[0])
    mean = np.mean(posarray)
    return mean
comp = 1300
enclast = 1300
# Complementary filter
def complementary(us_pos, enc_pos):
    global comp,enclast
    ####################################################
    # Lab 09 Task 3: Implement complementary filter.   #
    ####################################################
    pos = 0.03*us_pos + 0.97 *(comp+enc_pos-enclast)
    print(" COOOOOOOOOOOOOOMP", comp)
    enclast = enc_pos
    comp = pos
    return pos

# Draws a position from the ultrasonic sensor to the map.
def drawUS(pos):
    global curve_us
    x, y = curve_us.getData()
    x = np.append(x, pos)
    y = np.append(y, 700)
    curve_us.setData(x, y)

# Draws a moving average of the ultrasonic sensor position to the map.
def drawMovingAverageUS(pos):
    global curve_ma_us
    x, y = curve_ma_us.getData()
    x = np.append(x, pos)
    y = np.append(y, 600)
    curve_ma_us.setData(x, y)

# Draws a position from encoders to the map.
def drawEnc(pos):
    global curve_enc 
    x, y = curve_enc.getData()
    x = np.append(x, pos)
    y = np.append(y, 500)
    curve_enc.setData(x, y)

# Draws a complementary filtered result to the map.
def drawCompl(pos):
    global curve_compl
    x, y = curve_compl.getData()
    x = np.append(x, pos)
    y = np.append(y, 400)
    curve_compl.setData(x, y)

# Draws a position from a camera to the map.
def drawCam(pos):
    global curve_cam
    x, y = curve_cam.getData()
    x = np.append(x, pos)
    y = np.append(y, 300)
    curve_cam.setData(x, y)

# Draws a position from Kalman filter to the map.
def drawKalman(pos):
    global curve_kalman
    x, y = curve_kalman.getData()
    x = np.append(x, pos)
    y = np.append(y, 200)
    curve_cam.setData(x, y)

# Calculates velocity for a given sensor based on given position measurement.
def getVelocity(pos, sensor):
    ############################################################
    # Lab 09 Task 1: Calculate velocity for different sensors. #
    ############################################################
    global lastpos_us
    global lasttime_us
    global lastpos_cam
    global lasttime_cam
    global lastpos_enc
    global lasttime_enc
    global lastpos_us_ma
    global lasttime_us_ma
    global lastpos_comp
    global lasttime_comp
    global lastpos_kalman
    global lasttime_kalman
    ############################################################
    # Lab 09 Task 1: Calculate velocity for different sensors. #
    ############################################################
    ## velocity = distance/time
    velocity = 0

    timenow = time.time()
    if sensor == "Kalman":
        velocity = (lastpos_kalman-pos)/(timenow-lasttime_kalman)
        lasttime_kalman = timenow
        lastpos_kalman = pos
    if sensor == "Compl":
        velocity = (lastpos_comp-pos)/(timenow-lasttime_comp)
        lasttime_comp = timenow
        lastpos_comp = pos
    if sensor == "US_MA":
        velocity = (lastpos_us_ma-pos)/(timenow-lasttime_us_ma)
        lasttime_us_ma = timenow
        lastpos_us_ma = pos
    if sensor == "US":
        velocity = (lastpos_us-pos)/(timenow-lasttime_us)
        lasttime_us = timenow
        lastpos_us = pos

    if sensor == "Enc":
        velocity = (lastpos_enc - pos)/(timenow-lasttime_enc)
        lasttime_enc = timenow
        lastpos_enc = pos

    if sensor == "Cam":
        velocity = (lastpos_cam - pos)/(timenow-lasttime_cam)
        lasttime_cam = timenow
        lastpos_cam = pos

    return velocity
# Draws the velocity of the robot calculated from US measurements to the plot.
def drawUSVelocity(pos):
    global curve_us_vel, STARTTIME
    
    x, y = curve_us_vel.getData()
    velocity = getVelocity(pos, "US")
    x = np.append(x[1:], time.time()-STARTTIME)
    y = np.append(y[1:], velocity)
    curve_us_vel.setData(x, y)

# Draws the velocity of the robot calculated from US moving average measurements to the plot.
def drawMAUSVelocity(pos):
    global curve_ma_us_vel, STARTTIME
    
    x, y = curve_ma_us_vel.getData()
    velocity = getVelocity(pos, "US_MA")
    x = np.append(x[1:], time.time()-STARTTIME)
    y = np.append(y[1:], velocity)
    curve_ma_us_vel.setData(x, y)

# Draws the velocity of the robot calculated from encoder measurements to the plot.
def drawEncVelocity(pos):
    global curve_enc_vel, STARTTIME
    
    x, y = curve_enc_vel.getData()
    velocity = getVelocity(pos, "Enc")
    x = np.append(x[1:], time.time()-STARTTIME)
    y = np.append(y[1:], velocity)
    curve_enc_vel.setData(x, y)

# Draws the velocity of the robot calculated from complementary filtered results to the plot.
def drawComplVelocity(pos):
    global curve_compl_vel, STARTTIME
    
    x, y = curve_compl_vel.getData()
    velocity = getVelocity(pos, "Compl")
    x = np.append(x[1:], time.time()-STARTTIME)
    y = np.append(y[1:], velocity)
    curve_compl_vel.setData(x, y)

# Draws the velocity of the robot calculated from camera measurements to the plot.
def drawCamVelocity(pos):
    global curve_cam_vel, STARTTIME
    
    x, y = curve_cam_vel.getData()
    velocity = getVelocity(pos, "Cam")
    x = np.append(x[1:], time.time()-STARTTIME)
    y = np.append(y[1:], velocity)
    curve_cam_vel.setData(x, y)

# Draws the velocity of the robot calculated from camera measurements to the plot.
def drawKalmanVelocity(pos):
    global curve_kalman_vel, STARTTIME
    
    x, y = curve_kalman_vel.getData()
    velocity = getVelocity(pos, "Kalman")
    x = np.append(x[1:], time.time()-STARTTIME)
    y = np.append(y[1:], velocity)
    curve_kalman_vel.setData(x, y)

# Detects the green blob on the wall and returns its diameter in pixels
def getGreenBlobsize():

    hl=28
    hh=43
    sl=104
    sh=162
    vl=127
    vh=170

    ret, frame = cap.read()
    frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lowerLimits = np.array([hl, sl, vl])
    upperLimits = np.array([hh, sh, vh])
    thresholded = cv2.inRange(hsv, lowerLimits, upperLimits)
    outimage = cv2.bitwise_and(frame, frame, mask = thresholded)

    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.filterByColor = True
    params.filterByInertia = False
    params.filterByConvexity = False
    params.filterByCircularity = False
    params.minArea = 100
    params.maxArea = 100000
    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(cv2.bitwise_not(thresholded)) #list of blobs keypoints

    # Find and return the diameter of the largest blob
    max_size = 0
    for keypoint in keypoints:
        max_size = max(max_size, keypoint.size)
    ####################################################
    # Task 5.1: Implement green blob detection here    #
    ####################################################
    # ret, frame = cap.read()                          #
    # frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5) #
    # ......                                           #
    #################################################### 

    return max_size
def getDistanceWithCam(blob_size):
    if blob_size > 0:
        return 77480.8/blob_size - 154.2
    return -1
        ######################################################
        # Task 5.2: Calculate distance based on the bob size #
        ######################################################
        # distance = ...                                     #
        ######################################################


# Function to add two gaussians
def predict(mu1, sigma1, mu2, sigma2):
    ################################################################
    # Lab 09 Task 4.2: Implement the predict step.                 #
    ################################################################
    return (mu1+mu2,(sigma1**2+sigma2**2)**0.5)
# Function to multiply two gaussians
def update(mu1, sigma1, mu2, sigma2):
    ################################################################
    # Lab 09 Task 4.3: Implement the update step.                  #
    ################################################################
    mu = (mu1*sigma2**2 + mu2*sigma1**2)/(sigma1**2 + sigma2**2)
    sigma = (sigma1**2*sigma2**2/(sigma1**2+sigma2**2))**0.5
    return mu,sigma

# Slower code goes here
current_location_mu = None # This is the mean value for Gaussian representing our current location estimate in tasks 4.2 to 4.4
current_location_sigma = None # This is the standard deviation value for Gaussian representing our current location estimate in tasks 4.2 to 4.4
lastenc = 1300
def slowWorker():
    global us_pos, enc_pos, cam_pos, current_location_mu, current_location_sigma, plot2

    global lastenc
    # Get the blob size and convert it to distance from the wall
    blob_size = getGreenBlobsize()
    cam_pos = getDistanceWithCam(blob_size)
    
    # Adjust the x-coordinate range for plot2
    if CURRENT_LAB09_TASK >= 1:
        plot2.setXRange(time.time()-STARTTIME-5,time.time()-STARTTIME)

    # Update the graphs only when the values are valid
    if us_pos != None and CURRENT_LAB09_TASK < 4:
        drawUS(us_pos)
        if CURRENT_LAB09_TASK >= 1:
            drawUSVelocity(us_pos)
        if CURRENT_LAB09_TASK == 2:
            ma_pos = movingAverage(us_pos)
            drawMovingAverageUS(ma_pos)
            drawMAUSVelocity(ma_pos)
    
    if us_pos != None and enc_pos != None and CURRENT_LAB09_TASK == 3:
        compl_pos = complementary(us_pos, enc_pos)
        drawCompl(compl_pos)
        drawComplVelocity(compl_pos)

    if enc_pos != None and CURRENT_LAB09_TASK != 2:
        drawEnc(enc_pos)
        if CURRENT_LAB09_TASK >= 1:
            drawEncVelocity(enc_pos)

    if cam_pos != None and CURRENT_LAB09_TASK <= 1 or CURRENT_LAB09_TASK >= 4:
        drawCam(cam_pos)
        if CURRENT_LAB09_TASK >= 1:
            drawCamVelocity(cam_pos)
    
    camera_mu = None
    camera_sigma = None
    encoder_mu = None
    encoder_sigma = None
    ################################################################
    # Lab 09 Task 4.1: Update gaussians for camera and encoders.   #
    ################################################################
    if cam_pos != None:
        camera_mu = cam_pos
        camera_sigma = 55.6
    if enc_pos != None:
        encoder_mu = enc_pos - lastenc
        encoder_sigma = 10
        lastenc = enc_pos
    
    if CURRENT_LAB09_TASK >= 4:
        if camera_mu != None:
            plot_gaussian(camera_mu, camera_sigma, 0)
        if encoder_mu != None:
            plot_gaussian(encoder_mu, encoder_sigma, 1)
    
    #################################################################
    # Lab 09 Task 4.2                                               #
    # Initialize the current_location_mu and current_location_sigma #
    # parameters using a measurement from camera.                   #
    # Then update it on every encoder measurement.                  #
    #################################################################
    if CURRENT_LAB09_TASK == 4.2 or CURRENT_LAB09_TASK == 4.4:
        if current_location_mu == None:
            if cam_pos != None:
                current_location_mu = cam_pos
                current_location_sigma = 55.6
        else:
            current_location_mu, current_location_sigma = predict(current_location_mu, current_location_sigma, encoder_mu, encoder_sigma)

    #################################################################
    # Lab 09 Task 4.3                                               #
    # Initialize the current_location_mu and current_location_sigma #
    # parameters using a measurement from camera.                   #
    # Then update it on every new camera measurement.               #
    # Also stop the robot from moving                               #
    # by modifying your line following code.                        #
    #################################################################
    if CURRENT_LAB09_TASK >= 4.3:
        if camera_mu != None:
            if current_location_mu == None:
                current_location_mu, current_location_sigma = camera_mu, camera
            else:
                current_location_mu, current_location_sigma = update(current_location_mu,current_location_sigma,camera_mu,camera_sigma)
    #################################################################
    # Lab 09 Task 4.4                                               #
    # Put tasks 4.2 and 4.3 together.                               #
    #################################################################
    
    
    if current_location_mu != None:
        plot_gaussian(current_location_mu, current_location_sigma, 2)
        if CURRENT_LAB09_TASK == 4.4:
            drawKalman(current_location_mu)
            drawKalmanVelocity(current_location_mu)

# This function will be called when CTRL+C is pressed
def signal_handler(sig, frame):
    print('\nYou pressed Ctrl+C! Closing the program nicely :)')
    global running
    running = False
    try:
        ser.close()
    except Exception:
        pass
    sys.exit(0)

# Plots gaussian with given mu, sigma
def plot_gaussian(mu, sigma, gaussian_index):
    global gaussians
    x = np.arange(-200,2000)
    y = stats.norm.pdf(x, mu, sigma)
    gaussians[gaussian_index].setData(x, y)

# Register a callback for CTRL+C
signal.signal(signal.SIGINT, signal_handler)

# Create a window for plotting
win = pg.GraphicsWindow()
win.setWindowTitle('Plotter')
if CURRENT_LAB09_TASK < 1:
    win.resize(1024,480)
else:
    win.resize(1024,900)
plot1 = win.addPlot()
plot1.setLabel('top', "Distance (mm)")
plot1.setXRange(-200,2000)
plot1.setYRange(0,5000)
plot1.addLegend()
plot2 = None
if CURRENT_LAB09_TASK >= 4:
    win.nextRow()
    plot3 = win.addPlot()
    plot3.setXRange(-200,2000)
    plot3.addLegend()
if CURRENT_LAB09_TASK >= 1:
    win.nextRow()
    plot2 = win.addPlot()
    plot2.setLabel('top', "Velocity (mm/s)")
    plot2.addLegend()

# Initialize curves for each sensor
STARTTIME = time.time()
VEL_INIT_X = list(reversed([ -x*0.1 for x in range(50) ]))
VEL_INIT_Y = [0]*50
if CURRENT_LAB09_TASK < 4:
    curve_us = plot1.plot([], [], pen=pg.mkPen(width=5, color='r'), symbol='o', symbolBrush='r', symbolSize=15, name='Ultrasonic')
    if CURRENT_LAB09_TASK >= 1:
        curve_us_vel = plot2.plot(VEL_INIT_X[:], VEL_INIT_Y[:], pen=pg.mkPen(width=1, color='r'), name='Ultrasonic')
if CURRENT_LAB09_TASK <= 1 or CURRENT_LAB09_TASK >= 3:
    curve_enc = plot1.plot([], [], pen=pg.mkPen(width=5, color='g'), symbol='o', symbolBrush='g', symbolSize=15, name='Encoders')
    if CURRENT_LAB09_TASK >= 1:
        curve_enc_vel = plot2.plot(VEL_INIT_X[:], VEL_INIT_Y[:], pen=pg.mkPen(width=1, color='g'), name='Encoders')
if CURRENT_LAB09_TASK <= 1 or CURRENT_LAB09_TASK >= 4:
    curve_cam = plot1.plot([], [], pen=pg.mkPen(width=5, color='b'), symbol='o', symbolBrush='b', symbolSize=15, name='Camera')
    if CURRENT_LAB09_TASK >= 1:
        curve_cam_vel = plot2.plot(VEL_INIT_X[:], VEL_INIT_Y[:], pen=pg.mkPen(width=1, color='b'), name='Camera')
if CURRENT_LAB09_TASK == 2:
    curve_ma_us = plot1.plot([], [], pen=pg.mkPen(width=5, color=1), symbol='o', symbolBrush=1, symbolSize=15, name='Ultrasonic MA')
    curve_ma_us_vel = plot2.plot(VEL_INIT_X[:], VEL_INIT_Y[:], pen=pg.mkPen(width=1, color=1), name='Ultrasonic MA')
if CURRENT_LAB09_TASK == 3:
    curve_compl = plot1.plot([], [], pen=pg.mkPen(width=5, color=2), symbol='o', symbolBrush=2, symbolSize=15, name='Complementary')
    curve_compl_vel = plot2.plot(VEL_INIT_X[:], VEL_INIT_Y[:], pen=pg.mkPen(width=1, color=2), name='Complementary')
if CURRENT_LAB09_TASK >= 4.4:
    curve_kalman = plot1.plot([], [], pen=pg.mkPen(width=5, color='w'), symbol='o', symbolBrush='w', symbolSize=15, name='Kalman')
    curve_kalman_vel = plot2.plot(VEL_INIT_X[:], VEL_INIT_Y[:], pen=pg.mkPen(width=1, color='w'), name='Kalman')

# Initialize curves for Kalman filter
if CURRENT_LAB09_TASK >= 4:
    gaussian_names = ["Camera", "Encoders", "Filtered result"]
    gaussian_colors = ['b', 'g', 'w']
    gaussians = [ plot3.plot([], [], pen=pg.mkPen(width=1, color=gaussian_colors[i]), name=gaussian_names[i]) for i in range(3) ]

# Load a background image of a track
img_arr = np.asarray(cv2.cvtColor(cv2.imread('map.png'),cv2.COLOR_BGR2RGB))
img_item = pg.ImageItem(np.rot90(img_arr, -1))
img_item.scale(1.1, 10)
img_item.setZValue(-100)
plot1.addItem(img_item)

# Create global variables for the latest positions
us_pos = None
enc_pos = None
cam_pos = None

# open the camera
cap = cv2.VideoCapture(0)

running = True    # A state variable for keeping the fastWorker thread running
arduino_data = [] # This will be filled with decoded JSON data from Arduino

_thread.start_new_thread(fastWorker, ()) # Start fastWorker in a separate thread.

# Create timer and connect it to slowWorker.
# Effectively, slowWorker() will be called no more than 10 times per second.
timer = pg.QtCore.QTimer()
timer.timeout.connect(slowWorker)
timer.start(100)

# Execute the Qt application. This function is blocking until the user closes the window.
if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    QtGui.QApplication.instance().exec_()

# The window has been closed. Stop whatever we were doing.
running = False # Stop fastWorker
timer.stop()    # Stop slowWorker
ser.close()     # Disconnect from Arduino

