"""
Currently uses Jen's version of background subtraction. 

To run on the raspi: sudo python3 main.py 
If you want the verbose flag on run: sudo python3 main.py -v 
The verbose flag will print additional information like the current
postion of cloud according to the raspi. 

"""

import numpy as np
import cv2 as cv
import pygame
import sys, os, io
import RPi.GPIO as GPIO
from pygame.locals import *
from init import *
from Cloud import *
from picamera.array import PiRGBArray
from picamera import PiCamera
import time, serial, argparse, struct 


#Parse verbose flag
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", required=False, action="count", help="Verbose flag")
args = parser.parse_args()
verbose = False

if args.verbosity: 
    verbose = True

#Opens serial port to connect with arduino
try: 
    ser = serial.Serial(                         
        port = '/dev/ttyACM0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,  
        timeout=1
    )   
    if(ser.isOpen() == False):
        ser.open()
    time.sleep(1)
    if(verbose):
        print("Connection established succesfully!\n")
except Exception as e:
    print(e)

#Set output to hdmi if monitor connected 
os.environ["SDL_VIDEODRIVER"] = "fbcon"
os.environ["SDL_FBDEV"] = "/dev/fb0"

#Set up camera
camera = PiCamera()
camera.framerate = 10
camera.resolution = (1280, 736)
rawCapture = PiRGBArray(camera, size=(1280, 736))
time.sleep(0.1) #Let camera warm up

if(verbose):
    print("Camera initialized\n");

#Initialize frame/kernel for motion processing
first_frame = None
initial_image = None
kernel = np.ones((5,5), np.uint8)

#Initialize pygame display
pygame.init()
pygame.display.set_caption("Reach for the Sky")
try: 
    screen = pygame.display.set_mode([display_width, display_height])
except  pygame.error as message:
    if(verbose):
        print ("Cannot initialize display\n")
    raise SystemExit(message)


c = Cloud(0, 400, 350, 200) #initializes Cloud
counter = 0
ser.write(struct.pack('>B',0)); #send start message to arduino
if(verbose):
    print("Pygame initialzied\n");

try: 
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port = True):

        image = frame.array 
        
        if initial_image is None:
            initial_image = image

        diff = cv.absdiff(initial_image, image)
        gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(gray,(25,25),0)

        if first_frame is None:
            first_frame = gray
        
        frameDelta = cv.absdiff(first_frame, gray)
        diff = cv.threshold(frameDelta, 50, 255, cv.THRESH_BINARY)[1]
        diff = cv.dilate(diff, kernel, iterations=2)
        diff = cv.morphologyEx(diff, cv.MORPH_OPEN, kernel)
       	
        #displays image from picamera and cloud on top of it  
        img = display_frame(screen, diff)
        screen.blit(c.cloud,(c.xpos, c.ypos))
        

        c.update_pos(img)
        if(verbose):
            print(c.xpos) 
        
        if(c.stepper != 0 and counter > 5):
            counter = 0
            ser.write(struct.pack('>B', c.stepper)) #send xpos to arduino
            c.stepper = 0

        counter += 1

        if(ser.inWaiting() > 0): #print any messages from arduino
            line = ser.readline()
            print(int(line))
            #print(struct.unpack(">B", line))

        rawCapture.truncate(0) #clear stream for next picture
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE: #press space to change reference frame
                    if(verbose):
                        print("Switching frames\n")
                    initial_image = image
                    firstFrame = None
                else:
                    if(verbose):
                        print("Exiting program\n")
                    ser.close()
                    pygame.quit()
                
        pygame.display.update()

except KeyboardInterrupt: 
    ser.close()
    pygame.quit()
    if(verbose):
        print("Exiting program\n")

