# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import RPi.GPIO as GPIO



# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

coil_A_1_pin = 4 # pink
coil_A_2_pin = 17 # orange
coil_B_1_pin = 23 # blue
coil_B_2_pin = 24 # yellow
    
def initializeGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    #GPIO.setup(enable_pin, GPIO.OUT)
    GPIO.setup(coil_A_1_pin, GPIO.OUT)
    GPIO.setup(coil_A_2_pin, GPIO.OUT)
    GPIO.setup(coil_B_1_pin, GPIO.OUT)
    GPIO.setup(coil_B_2_pin, GPIO.OUT)

def setGPIO(w1, w2, w3, w4, holdTime):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_A_2_pin, w2)
    GPIO.output(coil_B_1_pin, w3)
    GPIO.output(coil_B_2_pin, w4)
    time.sleep(holdTime)
    
def moveRight(time):
    setGPIO(0,0,0,1,time)
    #setGPIO(0,0,0,0,1)
    
def moveLeft(time):
    setGPIO(0,0,1,0,time)
    #setGPIO(0,0,0,0,1)
    
def moveForward(time):
    setGPIO(0,0,1,1,time)
    #setGPIO(0,0,0,0,1)
    
def lookAround(time):
    setGPIO(0,0,1,0,time)

def processMovement(x,y):
    print("x: " + str(x) + " Y: " + str(y))
    if x < 200 :
        moveRight(.2)
    
    if x > 400 :
        moveLeft(.2)
        
    if x > 200 and x < 400 :
        print("moving forward")
        moveForward(.5)
        
    setGPIO(0,0,0,0,.01)


initializeGPIO()

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
#pts = deque(maxlen=args["buffer"])

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    
    
    if image is None:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    image = imutils.resize(image, width=600)
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    #cv2.imshow("hsv", hsv)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    #cv2.imshow("hsv", mask)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    #cv2.imshow("mask", mask)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 5:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(image, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(image, center, 5, (0, 0, 255), -1)
            processMovement(x,y)

    # update the points queue
    #pts.appendleft(center)
    
    # show the frame to our screen
    cv2.rectangle(image, (200,250),(400,500),(0,0,255),3)
    

    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break