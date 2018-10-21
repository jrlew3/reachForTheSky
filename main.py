import numpy as np
import cv2 as cv
import pygame
from pygame.locals import *
import sys

def display_frame(frame):
	frame = np.rot90(frame)
	frame = pygame.surfarray.make_surface(frame)
	screen.blit(frame,(0,0))

def exit():
	#Close windows
	cap.release()
	pygame.quit()
	cv.destroyAllWindows()

# Cloud variables 
cloud = pygame.image.load('cloud.png')
pygame.transform.scale(cloud, (100,250))
x = 0 
y = 0

#Initialize video feed
cap = cv.VideoCapture(0)
fgbg = cv.createBackgroundSubtractorMOG2()

ret, initial_frame = cap.read()

#Initialize pygame display
pygame.init()
pygame.display.set_caption("Reach for the Sky")
screen = pygame.display.set_mode([1280, 720])
#screen.fill([134,173,193])
screen.fill([0,0,0])

while(1):
	#Perform background subtraction
	ret, frame = cap.read( )
	
	diff = cv.absdiff(initial_frame, frame)
	#fgmask = fgbg.apply(frame)
	#cv.imshow('frame',fgmask)
	gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
	(thresh, diff) = cv.threshold(gray, 10, 255 , cv.THRESH_BINARY | cv.THRESH_OTSU)


	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if(event.key) == K_SPACE:
				ret, initial_frame = cap.read() 
				x += 1
			else:
				exit()

	display_frame(diff)
	screen.blit(cloud,(x,y))
	pygame.display.update()
	

exit()