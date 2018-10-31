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


"""

#Set up the GPIOS as outpets
GPIO.setmode(GPIO.BCM);
os.environ["SDL_FBDEV"] = "/dev/fb0"
os.putenv('SDL_FBDEV', '/dev/fb0')

os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
"""

#Set up camera
camera = PiCamera()
camera.framerate = 32
camera.resolution = (720, 1280)
rawCapture = PiRGBArray(camera, size=(720, 1280))
time.sleep(0.1) #Let camera warm up

"""
camera.capture(rawCapture, format="bgr")
initial_image = rawCapture.array
"""

#Initialize pygame display
pygame.init()
pygame.display.set_caption("Reach for the Sky")
screen = pygame.display.set_mode([display_width, display_height])
c = Cloud(0, 100, 350, 200)


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port = True):
	print("enter loop!")
	image = frame.array
	diff = cv.absdiff(initial_image, image)
	gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
	diff = cv.threshold(gray, bw_thresh, 255, cv.THRESH_BINARY)[1]

	screen.fill([0,0,0])
	img = display_frame(screen, diff)
	screen.blit(c.cloud,(c.xpos, c.ypos))
	c.update_pos(img)

	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_SPACE:
				initial_image = image
			else:
				exit()


	pygame.display.update()
	rawCapture.truncate(0)
	Rawcapture.seek(0)
exit()

