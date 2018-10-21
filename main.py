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
#screen.fill([134,173,193])


while(1):
	#Perform background subtraction
	ret, frame = cap.read( )
	
	diff = cv.absdiff(initial_frame, frame)
	gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
	(thresh, diff) = cv.threshold(gray, 10, 255 , cv.THRESH_BINARY | cv.THRESH_OTSU)

	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_SPACE:
				ret, initial_frame = cap.read() 
			else:
				exit(cap)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()

			if cloud_left.collidepoint(pos):

				if x <  display_width - step_size - cloud_width:  
					cloud_right.move_ip(step_size, 0)
					cloud_left.move_ip(step_size, 0)
					x += step_size
			if cloud_right.collidepoint(pos):
				if x > step_size:
					cloud_right.move_ip(-step_size, 0)
					cloud_left.move_ip(-step_size, 0)
					x -= step_size
				
	screen.fill([0,0,0])
	display_frame(screen, diff)
	screen.blit(cloud,(x,y))
	pygame.display.update()
	

exit(cap)