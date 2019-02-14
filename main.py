import numpy as np
import cv2
import time
import RPi.GPIO as io

io.setmode(io.BCM)
io.setwarnings(False)
coil_A_1_pin = 4 # pink
coil_A_2_pin = 17 # orange
coil_B_1_pin = 23 # blue
coil_B_2_pin = 24 # yellow
 
# adjust if different
StepCount = 8
Seq = range(0, StepCount)
Seq[0] = [0,1,0,0]
Seq[1] = [0,1,0,1]
Seq[2] = [0,0,0,1]
Seq[3] = [1,0,0,1]
Seq[4] = [1,0,0,0]
Seq[5] = [1,0,1,0]
Seq[6] = [0,0,1,0]
Seq[7] = [0,1,1,0]

delay = 1
steps = 5
 
#GPIO.setup(enable_pin, GPIO.OUT)
io.setup(coil_A_1_pin, io.OUT)
io.setup(coil_A_2_pin, io.OUT)
io.setup(coil_B_1_pin, io.OUT)
io.setup(coil_B_2_pin, io.OUT)
 
#GPIO.output(enable_pin, 1)
 
def setStep(w1, w2, w3, w4):
    io.output(coil_A_1_pin, w1)
    io.output(coil_A_2_pin, w2)
    io.output(coil_B_1_pin, w3)
    io.output(coil_B_2_pin, w4)
 
def forward(delay, steps):
    for i in range(steps):
        for j in range(StepCount):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)
 
def backwards(delay, steps):
    for i in range(steps):
        for j in reversed(range(StepCount)):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)


def detect_face(img):
    # convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # load OpenCV face detector, I am using LBP which is fast
    # there is also a more accurate but slow Haar classifier
    face_cascade = cv2.CascadeClassifier('opencv-files/lbpcascade_frontalface.xml')
    #face_cascade = cv2.CascadeClassifier('opencv-files/haarcascade_frontalface_alt.xml')

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
    setStep(0,0,0,0)

def send_signal(signal):
    if signal == 'move-right':
        backwards(int(delay) / 1000.0, int(steps))
    elif signal == 'move-left':
        forward(int(delay) / 1000.0, int(steps))
    else:
        clear_signal()
        
        

def process_recenter_face(rect):
    (x, y, w, h) = rect
    print(x)
    clear_signal()
    if x<100:
        print('move-left')
        send_signal('move-left')

    if x+w>250:
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
    face = cv2.resize(frame,(400,200))
    rect = None
    
    face, rect = detect_face(face)

    #print(rect)
    clear_signal()	
    if rect is not None:
    	#frame = draw_rectangle(frame, rect)
    	process_recenter_face(rect)
    	#cv2.imshow("preview", draw_rectangle(frame,rect))
    	cv2.imshow("preview", frame)
    else:
        cv2.imshow("preview", frame)


    key = cv2.waitKey(1)
    if key == 27:  # exit on ESC
        print("escape")
        break
    else:
        cv2.line(img=frame, pt1=(10, 10), pt2=(100, 10), color=(255, 0, 0), thickness=5, lineType=8, shift=0)
vc.release()
cv2.destroyWindow("preview")
