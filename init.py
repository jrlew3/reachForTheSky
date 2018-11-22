import numpy as np
import cv2 as cv
import pygame
import sys
from pygame.locals import *

thresh = 20  # the change in color required to move the cloud 
bw_thresh = 50 # the threshold used in converting image to BW

display_width = 1280
display_height = 736


def display_frame(screen, frame):
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame) #convert image into a pygame surface
    screen.blit(frame,(0,0))
    return frame

def get_brightness(color):
    return color[0] + color[1] + color[2]
