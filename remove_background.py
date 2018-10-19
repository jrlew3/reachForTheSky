import numpy as np
import cv2 as cv
import pygame
from pygame.locals import *
import sys
"""

cap = cv2.VideoCapture(0)
pygame.init()
pygame.display.set_caption("Reach for the Sky")
screen = pygame.display.set_mode([1280,720])

try:
	while True:
			ret, frame = cap.read()

			screen.fill([0,0,0])
			frame = cv2.cvtColor((frame, cv2.COLOR_BGR2RGB))
			frame = np.rot90(frame)
			frame = pygame.surfarray.make_surface(frame)
			screen.blit(frame, (0,0))
			pygame.display.update()

			for event in pygame.event.get():
				if event.type == KEYDOWN:
					sys.exit(0)

except KeyboardInterrupt: 
	pygame.quit()
	cv2.destroyAllWindows()


"""   
cap = cv.VideoCapture(0)
fgbg = cv.createBackgroundSubtractorMOG2()
while(1):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    cv.imshow('frame',fgmask)
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()


