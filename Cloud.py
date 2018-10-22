import numpy as np
import cv2 as cv
import pygame
import sys
from pygame.locals import *


class Cloud: 
	def __init__(self, xpos, ypos, width, height):
		self.xpos = xpos
		self.ypos = ypos
		self.x = 0
		self.y = 0
		self.width = width
		self. height = height
		
		self.cloud = pygame.image.load('cloud.png')
		self.cloud = pygame.transform.scale(self.cloud, (self.width,self.height))
		self.right = pygame.Rect(self.xpos + self.width/2, self.ypos, self.width/2, self.height)
		self.left = pygame.Rect(self.xpos, self.ypos, self.width/2, self.height)
		self.up = pygame.Rect(self.xpos, self.ypos, self.width, self.height/2)
		self.down = pygame.Rect(self.xpos, self.ypos + self.height/2, self.width, self.height/2) 

		self.stepsize = 10
		self.driftsize = 2


	def move(self):
		self.right.move_ip(x,y)
		self.left.move_ip(x,y)
		self.up.move_ip(x,y)
		self.down.move_ip(x,y)
		self.xpos += self.x
		self.ypos += self.y

	def check_region(self, region, image): 
		if region == "left":
			subcloud = self.left
		elif region == "right":
			subcloud = self.right
		elif region == "up"
			subcloud = self.up
		elif region == "down":
			subcloud = self.down 

		avg_color = pygame.transform.average_color(image, subcloud)
		return get_brightness(avg_color) > thresh 


	def check_movement(self, image):
		if self.check_region("left", image):
			if self.xpos <  display_width - self.stepsize - self.width:  
				self.x = stepsize
		elif self.check_region("right", image):
			if self.xpos > stepsize:
				self.x = -stepsize
		if self.check_region("up", image):
			if self.ypos < display_height - self.stepsize - self.height:
				self.y = stepsize
		elif self.check_region("down", image):
			if self.ypos > self.stepsize:
				self.y = -stepsize

	def drift(self): 
		if self.x != 0 or self.y != 0: 
			self.move(self.x, self.y)
			self.x = 0 
			self.y = 0
			print("move the clouds \n")
		elif self.xpos <= self.driftsize:
			self.driftsize = abs(self.driftsize)
			print("change to right\n")
		elif self.xpos < display_width - self.width - self.driftsize: 
			self.xpos += self.driftsize 
			self.move(driftsize, 0)
			if 0 < self.driftsize:
				print("move right\n")
			else:
				print("move left\n")
		else: 
			self.driftsize = -abs(self.driftsize)
			print("change to left\n")
			






