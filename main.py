import numpy as np
import cv2


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


def process_recenter_face(rect):
    (x, y, w, h) = rect
    #print(x)
    if x<300:
        print('move-left')

    if x>600:
        print('move-right')




cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:

    rval, frame = vc.read()

    face, rect = detect_face(frame)

    # if rect is not None:
    #     frame = draw_rectangle(frame, rect)
    #     process_recenter_face(rect)

    cv2.imshow("preview", frame)


    key = cv2.waitKey(100)
    if key == 27:  # exit on ESC
        print("escape")
        break
    else:
        cv2.line(img=frame, pt1=(10, 10), pt2=(100, 10), color=(255, 0, 0), thickness=5, lineType=8, shift=0)
vc.release()
cv2.destroyWindow("preview")