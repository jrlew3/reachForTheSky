import io 
import time
import picamera


with picamera.PiCamera() as camera:
	stream = io.BytesIO()
	for frame in camera.capture_continuous(stream, format="bgr", use_video_port=True):
		stream.truncate()
		stream.seek(0)
 
