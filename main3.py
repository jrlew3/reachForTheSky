"""
Face Tracking version 
"""

import numpy as np
import cv2
import sys, os, io
import RPi.GPIO as GPIO
from init import *
from Cloud import *
from picamera.array import PiRGBArray
from picamera import PiCamera
import time, serial, argparse, struct



def detectFace(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30,30),
    )
    
    if(verbose) 
        print("Detecting face")
    
    maxArea = 0
    xpos = 0
    ypos = 0 
    width = 0
    height = 0
    
    # Send largest face
    for (x,y,w, h) in faces:
        if w*h > maxArea:
            xpos = int(x)
            ypos = int(y)
            width = int(w)
            hieght = int(h)
            maxArea = w*h

    if maxArea > 0:
        bbox = (xpos, ypos, width, height)
        return bbox
    
    return None
    

def updateStepper(currPos, delta):
    stepperPos = int(ser.readline())
    print("Message from Arduino: ", stepperPos)

    if abs(stepperPos - currPos) < delta:
        currDirection = 0
    elif stepperPos <= currPos:
        currDirection = 1
    else: 
        currDirection = -1
    
    if(currDirection != stepperDirection):
       stepperDirection = currDirection 
       ser.write(struct.pack('>B', currDirection))

        


# Parse verbose flag
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", required=False, action="count", help="Verbose flag")
args = parser.parse_args()
verbose = False

if args.verbosity:
    verbose = True

# Open serial port to connect with Arduino
try: 
    ser = serial.Serial(
        port = '/dev/ttyACM0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
    if not ser.isOpen():
        ser.open()
        time.sleep(1)
except as Exception as e:
    preint(e)

 
# Initialize tracker 
trackingFace = 0 # Does not track face to begin with 
tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
tracker_type = tracker_types[6]
if tracker_type == 'MOSSE':
    tracker = cv2.TrackerMOSSE_create()

# Initialize face detection 
faceCascade = cv2.CascadeClassifier("/data/haarcascades/haarcascade_frontalface_alt.xml")

# Set up display
os.environ["SDL_VIDEODRIVER"] = "fbcon"
os.environ["SDL_FBDEV"] = "/dev/fb0" #use hdmi port

# Set up camera
camera = PiCamera()
camera.frameRate = 5
camera.resolution = (1280, 736)
rawCapture = PiRGBArray(camera, size=(1280,736))
time.sleep(0.1)

# Initialize arduino variables
stepperDirection = 0
ser.write(struct.pack('>B', 0)); #send start message to arduino




# ------------------------ BEGINNING OF MAIN LOOP ----------------------- #

for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = image.array
    if(verbose)
        print(Reset loop)

    # Get fps
    """
    timer = cv2.getTickCount()
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    if(verbose)
        print("FPS:", fps)
    """

    # Initialize tracker 
    if not trackingFace:
        bbox = detectFace(frame)
        if bbox is not None: 
            tracker.init(frame, bbox)
            trackingFace = 1

    if trackingFace:
        print("Tracking face")
        ok, bbox = tracker.update(frame)
        if not ok: 
            trackingFace = 0
            continue

        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255,0,0),2,1)
        """
        # image, center, radius, color, thickness, linetype, shift
        xpos = int(bbox[0] + bbox[2]/2)
        ypos = int(bbox[1])
        cv2.circle(frame, xpos, ypos, 10, (0,0,255), -1) 
        """

        if(ser.inWaiting() > 0):
            currPos = int(bbox[0] + bbox[2]/2)
            delta = bbox[2]/4
            updateStepper(currPos, delta)

    
    #cv2.imshow("Tracking", frame)
    rawCapture.truncate(0) #clear stream for next picture
    
       
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

ser.close()


