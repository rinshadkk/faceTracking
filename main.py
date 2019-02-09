import numpy as np
import cv2
import time
import RPi.GPIO as io

io.setmode(io.BCM)

relay1_pin = 23
relay2_pin = 22

io.setup(relay1_pin,io.OUT)
io.setup(relay2_pin,io.OUT)
io.output(relay1_pin,True)
io.output(relay2_pin,True)


def detect_face(img):
    # convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # load OpenCV face detector, I am using LBP which is fast
    # there is also a more accurate but slow Haar classifier
    face_cascade = cv2.CascadeClassifier('opencv-files/lbpcascade_frontalface.xml')

    # let's detect multiscale (some images may be closer to camera than others) images
    # result is a list of faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);

    # if no faces are detected then return original img
    if (len(faces) == 0):
        return None, None

    # under the assumption that there will be only one face,
    # extract the face area
    (x, y, w, h) = faces[0]

    # return only the face part of the image
    return gray[y:y + w, x:x + h], faces[0]



def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    return cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

def clear_signal():
    io.output(relay1_pin,True)
    io.output(relay2_pin,True)

def send_signal(signal):
    if signal == 'move-left':
        io.output(relay1_pin,False)
        io.output(relay2_pin,True)
    elif signal == 'move-right':
        io.output(relay1_pin,True)
        io.output(relay2_pin,False)
    else:
        clear_signal()
        
        

def process_recenter_face(rect):
    (x, y, w, h) = rect
    print(x)
    clear_signal()
    if x<200:
        print('move-left')
        send_signal('move-left')

    if x>300:
        print('move-right')
        send_signal('move-right')




cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:

    rval, frame = vc.read()

    face, rect = detect_face(frame)

    #print(rect)
    clear_signal()	
    if rect is not None:
    	#frame = draw_rectangle(frame, rect)
    	process_recenter_face(rect)


    #cv2.imshow("preview", cv2.resize(frame,(600,400)))


    key = cv2.waitKey(1)
    if key == 27:  # exit on ESC
        print("escape")
        break
    else:
        cv2.line(img=frame, pt1=(10, 10), pt2=(100, 10), color=(255, 0, 0), thickness=5, lineType=8, shift=0)
vc.release()
cv2.destroyWindow("preview")
