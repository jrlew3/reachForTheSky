import numpy as np
import cv2 as cv
import pygame
import sys
from pygame.locals import *

thresh = 10  # the change in color required to move the cloud 
bw_thresh = 50

display_width = 1280
display_height = 720


def display_frame(screen, frame):
	frame = np.rot90(frame)
	frame = pygame.surfarray.make_surface(frame)
	screen.blit(frame,(0,0))
	return frame

def exit():
	#Close windows
	pygame.quit()

def get_brightness(color):
	return color[0] + color[1] + color[2]
