import numpy as np
import cv2 as cv
import pygame
import sys
import os 
import RPi.GPIO as GPIO
from pygame.locals import *
from init import *
from Cloud import *
from picamera.array import PiRGBArray
from picamera import PiCamera
import time 
import io 
import serial 
import argparse
import struct 

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
camera.framerate = 2
camera.resolution = (256, 160)
rawCapture = PiRGBArray(camera, size=(256, 160))
time.sleep(0.1) #Let camera warm up

#Take initial reference frame
camera.capture(rawCapture, format="bgr")
initial_image = rawCapture.array
rawCapture.truncate(0)
if(verbose):
    print("Camera initialized\n");


#Initialize pygame display
pygame.init()
pygame.display.set_caption("Reach for the Sky")

counter = 0

try: 
    screen = pygame.display.set_mode([display_width, display_height])
except  pygame.error as message:
    if(verbose):
        print ("Cannot initialize display\n")
    raise SystemExit(message)

if(verbose):
    print("display intialized\n")
c = Cloud(0, 10, 35, 20) #initializes Cloud

print("Pygame initialzied\n");

try: 
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port = True):

        image = frame.array
        diff = cv.absdiff(initial_image, image)
        gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
        diff = cv.threshold(gray, bw_thresh, 255, cv.THRESH_BINARY)[1]

       	#displays image from picamera and cloud on top of it  
        img = display_frame(screen, diff)
        screen.blit(c.cloud,(c.xpos, c.ypos))
        
        c.update_pos(img)
        if(verbose):
            print(c.xpos) 
        
        if(counter > 10):
            counter = 0
            ser.write(struct.pack('>B', c.xpos)) #send xpos to arduino
        
        counter += 1

        if(ser.inWaiting() > 0): #print any messages from arduino
            line = ser.readline()
            print(line)
            #if(verbose):
                #print(line)

        rawCapture.truncate(0) #clear stream for next picture
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE: #press space to change reference frame
                    initial_image = image
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

