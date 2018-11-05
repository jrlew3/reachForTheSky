import numpy as np
import cv2 as cv
import pygame
import sys
from pygame.locals import *
from init import *
import copy
import cv2
import serial

from Cloud import *

#Initialize video feed
cap = cv.VideoCapture(0)
ret, initial_frame = cap.read()

#Initialize pygame display
pygame.init()
pygame.display.set_caption("Reach for the Sky")
screen = pygame.display.set_mode([display_width, display_height])
c = Cloud(0, 100, 350, 200)

#Initialisze frame/kernel for motion processing
firstFrame = None
kernel = np.ones((5, 5), np.uint8)

while 1:
	ret, frame = cap.read( )
	
	diff = cv.absdiff(initial_frame, frame)
	gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
	gray = cv.GaussianBlur(gray, (25,25), 0)

	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		continue

	frameDelta = cv.absdiff(firstFrame, gray)
	diff = cv.threshold(frameDelta, 25, 255, cv.THRESH_BINARY)[1]
	diff = cv.dilate(diff, kernel, iterations=2)
	diff = cv.morphologyEx(diff, cv.MORPH_OPEN, kernel)

	screen.fill([0,0,0])
	image = display_frame(screen, diff)
	screen.blit(c.cloud,(c.xpos, c.ypos))
	c.update_pos(image)

	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_SPACE:
				ret, initial_frame = cap.read()
				firstFrame = None
			else:
				exit(cap)

	# press q to quit
	key = cv.waitKey(1) & 0xFF
	if key == ord("q"):
		break

	pygame.display.update()


exit(cap)
