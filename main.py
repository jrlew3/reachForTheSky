import numpy as np
import cv2 as cv
import pygame
import sys
from pygame.locals import *
from init import *
from Cloud import *

#Initialize video feed
cap = cv.VideoCapture(0)
ret, initial_frame = cap.read()

#Initialize pygame display
pygame.init()
pygame.display.set_caption("Reach for the Sky")
screen = pygame.display.set_mode([display_width, display_height])
c = Cloud(0, 100, 350, 200)


while(1):
	ret, frame = cap.read( )
	
	diff = cv.absdiff(initial_frame, frame)
	gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
	diff = cv.threshold(gray, bw_thresh, 255, cv.THRESH_BINARY)[1]

	screen.fill([0,0,0])
	image = display_frame(screen, diff)
	screen.blit(c.cloud,(c.xpos, c.ypos))
	c.update_pos(image)

	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_SPACE:
				ret, initial_frame = cap.read() 
			else:
				exit(cap)


	pygame.display.update()
	

exit(cap)

