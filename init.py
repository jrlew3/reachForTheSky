import numpy as np
import cv2 as cv
import pygame
import sys
from pygame.locals import *

cloud_width = 350
cloud_height = 200
cloud = pygame.image.load('cloud.png')
cloud = pygame.transform.scale(cloud, (cloud_width,cloud_height))
cloud_right = pygame.Rect(cloud_width/2, 0, cloud_width/2, cloud_height)
cloud_left = pygame.Rect(0, 0, cloud_width/2, cloud_height)


x = 0 
y = 0
step_size = 20

display_width = 1280
display_height = 720

def display_frame(screen, frame):
	frame = np.rot90(frame)
	frame = pygame.surfarray.make_surface(frame)
	screen.blit(frame,(0,0))

def exit(cap):
	#Close windows
	cap.release()
	pygame.quit()
	cv.destroyAllWindows()


