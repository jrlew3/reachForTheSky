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
    print("Connection established succesfully!\n")
except Exception as e:
    print(e)

os.environ["SDL_VIDEODRIVER"] = "fbcon"


#Set up the GPIOS as outpets
#GPIO.setmode(GPIO.BCM);

os.environ["SDL_FBDEV"] = "/dev/fb0"
os.putenv('SDL_FBDEV', '/dev/fb0')

"""
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')


drivers = ['fbcon', 'fbi', 'fbturbo', 'directfb', 'svgalib']
found = False
for driver in drivers:
    if not os.getenv('SDL_VIDEODRIVER'):
        os.putenv('SDL_VIDEODRIVER', driver)
    try:
        pygame.display.init()
    except pygame.error:
        print ('Driver failed')
        continue
    found = True
    break

"""   


#Set up camera
camera = PiCamera()
camera.framerate = 32
camera.resolution = (1024, 768)
rawCapture = PiRGBArray(camera, size=(1024, 768))
time.sleep(0.1) #Let camera warm up

camera.capture(rawCapture, format="bgr")
initial_image = rawCapture.array
rawCapture.truncate(0)
print("Camera initialized\n");


#Initialize pygame display
pygame.init()
pygame.display.set_caption("Reach for the Sky")

try: 
    screen = pygame.display.set_mode([display_width, display_height])
except  pygame.error as message:
    print ("Cannot initialize display\n")
    raise SystemExit(message)

print("display intialized\n")
c = Cloud(0, 100, 350, 200)

print("Pygame initialzied\n");

try: 
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port = True):

        image = frame.array
        diff = cv.absdiff(initial_image, image)
        gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
        diff = cv.threshold(gray, bw_thresh, 255, cv.THRESH_BINARY)[1]

        screen.fill([0,0,0])
        img = display_frame(screen, diff)
        screen.blit(c.cloud,(c.xpos, c.ypos))
        c.update_pos(img)
        
        print(c.xpos) 
        ser.write(bytes(c.xpos, 'utf-8'))
        if(ser.inWaiting() > 0):
            line = ser.readline()
            print(line)

        rawCapture.truncate(0)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    #print("Change background image \n")
                    initial_image = image
                else:
                    print("Exiting program\n")
                    ser.close()
                    exit()
                
        pygame.display.update()

except KeyboardInterrupt: 
    ser.close()
    pygame.quit()
    print("Exiting program\n")

ser.close()
print("Successfully closed serial\n");


exit()

