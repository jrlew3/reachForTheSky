from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100, help="# frames to loop over test")
ap.add_argument("-d", "--display", type=int, default=-1, help="Whether to display frames")
args = vars(ap.parse_args())

os.environ["SDL_VIDEODRIVER"] = "fbcon"
os.environ["SDL_FBDEV"] = "/dev/fb0"
os.putenv('SDL_FBDEV', '/dev/fb0')

camera = PiCamera()
camera.resolution = (320,240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size =(320,240))
stream = camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)

print("[INFO] sampling frames from picamera module")
vs = PiVideoStream().start()
time.sleep(2.0)
fps = FPS().start()

while fps._numFrames < args["num_frames"]:
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    if args["display"] > 0:
        cv2.imshow("frame", frame)
        key = cv2.waitKey(1) & 0xff

    fps.update()

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()

