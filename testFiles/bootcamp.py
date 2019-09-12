import numpy as np
import cv2
import time as time
blobparams = cv2.SimpleBlobDetector_Params()
blobparams.filterByColor = True
blobparams.blobColor = 255
blobparams.filterByArea = True
blobparams.filterByCircularity = False
blobparams.filterByConvexity = False
blobparams.filterByInertia = False
blobparams.minDistBetweenBlobs = 100
blobparams.minArea = 300
blobparams.maxArea = 20000
detector = cv2.SimpleBlobDetector_create(blobparams)

"""trackbar_value = 30
trackbar_value2 = 39
trackbar_value3 = 83
trackbar_value4 = 84
trackbar_value5= 255
trackbar_value6= 255
try:
	f = open("thresh.txt", "r")
	trackbar_value = int(f.readline().rstrip())
	trackbar_value2 = int(f.readline().rstrip())
	trackbar_value3 = int(f.readline().rstrip())
	trackbar_value4 = int(f.readline().rstrip())
	trackbar_value5 = int(f.readline().rstrip())
	trackbar_value6 = int(f.readline().rstrip())
	f.close()
except:
	pass


def updateValue(value):
        global trackbar_value
        trackbar_value = value
        return
def updateValue2(value):
        global trackbar_value2
        trackbar_value2 = value
        return
def updateValue3(value):
        global trackbar_value3
        trackbar_value3 = value
        return
def updateValue4(value):
        global trackbar_value4
        trackbar_value4 = value
        return
def updateValue5(value):
        global trackbar_value5
        trackbar_value5 = value
        return
def updateValue6(value):
        global trackbar_value6
        trackbar_value6 = value
        return



cv2.namedWindow("Trackbars")
cv2.createTrackbar("lH","Trackbars",trackbar_value,255,updateValue)
cv2.createTrackbar("lS","Trackbars",trackbar_value2,255,updateValue2)
cv2.createTrackbar("lV","Trackbars",trackbar_value3,255,updateValue3)
cv2.createTrackbar("HH","Trackbars",trackbar_value4,255,updateValue4)
cv2.createTrackbar("HS","Trackbars",trackbar_value5,255,updateValue5)
cv2.createTrackbar("HV","Trackbars",trackbar_value6,255,updateValue6)"""
cap = cv2.VideoCapture(2)
fps = 0
frame_counter = 0
frame_counter_start = time.time()
while True:
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lowerLimits = np.zeros(3)
    upperLimits = np.zeros(3)
    f = open("thresh.txt", "r")
    for i in range(3):
        lowerLimits[i] = int(f.readline().strip())
    for i in range(3):
        upperLimits[i] = int(f.readline().strip())

    thresholded = cv2.inRange(frame, lowerLimits, upperLimits)
    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(thresholded,cv2.MORPH_OPEN,kernel)

    coordinates = detector.detect(thresholded)
    for coordinate in coordinates:
        cv2.putText(frame, str(coordinate.pt[0]) + " " + str(coordinate.pt[1]),
                    (int(coordinate.pt[0]), int(coordinate.pt[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    for i in range(3):
        lowerLimits[i] = int(f.readline().strip())
    for i in range(3):
        upperLimits[i] = int(f.readline().strip())
    thresholded = cv2.inRange(frame, lowerLimits, upperLimits)
    opening = cv2.morphologyEx(thresholded, cv2.MORPH_OPEN, kernel)
    coordinates = detector.detect(thresholded)
    for coordinate in coordinates:
        cv2.putText(frame, str(coordinate.pt[0]) + " " + str(coordinate.pt[1]),
                    (int(coordinate.pt[0]), int(coordinate.pt[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    frame_counter += 1

    if frame_counter % 10 == 0:
        frame_counter_end = time.time()
        fps = int(10 / (frame_counter_end - frame_counter_start))
        frame_counter = 0
        frame_counter_start = time.time()

    cv2.putText(frame, str(fps), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

    cv2.imshow('thresholded', opening)
    cv2.imshow('Original', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        f.close()
        break

cap.release()
cv2.destroyAllWindows()

