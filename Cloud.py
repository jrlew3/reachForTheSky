import numpy as np
import cv2 as cv
import pygame
import sys
from pygame.locals import *
from init import *


class Cloud: 
	def __init__(self, xpos, ypos, width, height):
		self.xpos = xpos #the current x position of the cloud 
		self.ypos = ypos 
		self.x = 0 #the change in x position of the cloud
		self.y = 0
		self.width = width
		self. height = height
		self.direction = 1 #1 for right, -1 for left
		
		self.cloud = pygame.image.load('cloud.png')
		self.cloud = pygame.transform.scale(self.cloud, (self.width,self.height))
		self.right = pygame.Rect(self.xpos + self.width/2, self.ypos, self.width/2, self.height)
		self.left = pygame.Rect(self.xpos, self.ypos, self.width/2, self.height)
		self.up = pygame.Rect(self.xpos, self.ypos, self.width, self.height/2)
		self.down = pygame.Rect(self.xpos, self.ypos + self.height/2, self.width, self.height/2) 

		self.stepsize = 5 
		self.driftsize = 1

	def move(self):
		self.right.move_ip(self.x,self.y) #moves cloud in place by x and y
		self.left.move_ip(self.x,self.y)
		self.up.move_ip(self.x,self.y)
		self.down.move_ip(self.x,self.y)
		self.xpos += self.x #update x position
		self.ypos += self.y
		self.x = 0 #reset distance to move to zero 
		self.y = 0 

	""" 
	Checks for collision in the specified region by getting the average color of the 
	background. If the lightness value of the color is above the threshold, then 
	check_region will return True. Otherwise, it will return false. The sensitivity is set by 
	the variable thresh which can be found in init.py. The get_brightness function
	can be found in init.py.

	Assumes that the background is black and any figure will apear white. 
	"""

	def check_region(self, region, image): 
		if region == "left":
			subcloud = self.left
		elif region == "right":
			subcloud = self.right
		elif region == "up":
			subcloud = self.up
		elif region == "down":
			subcloud = self.down 

		avg_color = pygame.transform.average_color(image, subcloud)
		return get_brightness(avg_color) > thresh 

	"""
	Checks for collision in each of the regions (left, right, up, down) and updates
	the direction and change in position needed to move cloud. If collision is 
	detected in a region, then the cloud will move in the oppositie direction with 
	a change in position set by the stepsize unless the cloud is about to move 
	offscreen in which case the cloud will change direction. 
	"""

	def check_movement(self, image):
		if self.check_region("left", image):
			if self.xpos <  display_width - self.stepsize - self.width: #checks if going offscreen
				self.x = self.stepsize
				self.direction = 1
		elif self.check_region("right", image):
			if self.xpos > self.stepsize:
				self.x = -self.stepsize
				self.direction = -1
		if self.check_region("up", image):
			if self.ypos < display_height - self.stepsize - self.height:
				self.y = self.stepsize
		elif self.check_region("down", image):
			if self.ypos > self.stepsize:
				self.y = -self.stepsize
	
	"""
	If there is no change in position, the cloud will automatically "drift" in the 
	correct direction
	"""
	def drift(self): 
		if self.x == 0 and self.y == 0: 
			if self.xpos <= self.driftsize:
				self.direction = 1
			elif self.xpos >= display_width - self.width - self.driftsize: 
				self.direction = -1
			self.x = self.direction * self.driftsize
		
		self.move()

	def update_pos(self, image):
		self.check_movement(image)
		self.drift()


