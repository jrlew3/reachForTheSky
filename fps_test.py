from __future__ import print_function
from imutils.video import VideoStream
import datetime
import argparse
import imutils
import cv2
import time 
import numpy as np
import os, io, sys

os.environ["SDL_VIDEODRIVER"] = "fbcon"
os.environ["SDL_FBDEV"] = "/dev/fb0"
os.putenv('SDL_FBDEV', '/dev/fb0')
frameSize = (320, 240)

vs = VideoStream(usePiCamera=1 > 0).start() 
time.sleep(2.0)

while 1:
    frame = vs.read()
    
    timestamp = datetime.datetime.now()
    
    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1) & 0xff
    
    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()
