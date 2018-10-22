import numpy as np
import cv2 as cv
import pygame
import sys
from pygame.locals import *

cloud_width = 350
cloud_height = 200
cloudx = 0
cloudy = 100
x = 0
y = 0
stepsize = 10
driftsize = 2

cloud = pygame.image.load('cloud.png')
cloud = pygame.transform.scale(cloud, (cloud_width,cloud_height))
cloud_right = pygame.Rect(cloudx + cloud_width/2, cloudy, cloud_width/2, cloud_height)
cloud_left = pygame.Rect(cloudx, cloudy, cloud_width/2, cloud_height)
cloud_up = pygame.Rect(cloudx, cloudy, cloud_width, cloud_height/2)
cloud_down = pygame.Rect(cloudx, cloudy +cloud_height/2, cloud_width, cloud_height/2) 
threshold = 2  # the change in color required to move the cloud 
bw_thresh = 50

display_width = 1280
display_height = 720


def display_frame(screen, frame):
	frame = np.rot90(frame)
	frame = pygame.surfarray.make_surface(frame)
	screen.blit(frame,(0,0))
	return frame

def exit(cap):
	#Close windows
	cap.release()
	pygame.quit()
	cv.destroyAllWindows()

def move_clouds(x, y):
	global cloudx, cloudy
	global cloud_right, cloud_left, cloud_up, cloud_down
	cloud_right.move_ip(x,y)
	cloud_left.move_ip(x,y)
	cloud_up.move_ip(x,y)
	cloud_down.move_ip(x,y)
	cloudx += x
	cloudy += y

def get_brightness(color):
	return (color[0] + color[1] + color[2])/3

def check_movement(direction, image):

	if direction == "left":
		subcloud = cloud_left
	if direction == "right":  
		subcloud = cloud_right
	if direction == "up":
		subcloud = cloud_up
	if direction == "down":
		subcloud = cloud_down

	avg_color = pygame.transform.average_color(image, subcloud)
	return get_brightness(avg_color) > threshold 
