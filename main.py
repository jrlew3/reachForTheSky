import numpy as np
import cv2 as cv
import pygame
import sys
from pygame.locals import *
from init import *

#Initialize video feed
cap = cv.VideoCapture(0)

ret, initial_frame = cap.read()

#Initialize pygame display
pygame.init()
pygame.display.set_caption("Reach for the Sky")
screen = pygame.display.set_mode([display_width, display_height])


while(1):
	ret, frame = cap.read( )
	
	diff = cv.absdiff(initial_frame, frame)
	gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)

	thresh = 50
	diff = cv.threshold(gray, thresh, 255, cv.THRESH_BINARY)[1]
	#(thresh, diff) = cv.threshold(gray, 10, 255 , cv.THRESH_BINARY | cv.THRESH_OTSU)
	#cv.imshow("diff", gray)
	screen.fill([0,0,0])
	image = display_frame(screen, diff)
	screen.blit(cloud,(cloudx, cloudy))

	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_SPACE:
				ret, initial_frame = cap.read() 
			else:
				exit(cap)

	if check_movement("left", image):
		if cloudx <  display_width - stepsize - cloud_width:  
			x = stepsize
	elif check_movement("right", image):
		if cloudx > stepsize:
			x = -stepsize
	if check_movement("up", image):
		if cloudy < display_height - stepsize - cloud_height:
			y = stepsize
	elif check_movement("down", image):
		if cloudy > stepsize:
			y = -stepsize



	if x != 0 or y != 0:
		cloud_right.move_ip(x,y)
		cloud_left.move_ip(x,y)
		cloud_up.move_ip(x,y)
		cloud_down.move_ip(x,y)
		cloudx += x
		cloudy += y

		x = 0
		y = 0

	pygame.display.update()
	

exit(cap)

