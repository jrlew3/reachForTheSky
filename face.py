import cv2
import sys
from time import sleep 


#faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
#faceCascade = cv2.CascadeClassifier("haarcascade_eye.xml")
faceCascade = cv2.CascadeClassifier("data/haarcascades/haarcascade_frontalface_alt.xml")
video_capture = cv2.VideoCapture(0)
anterior = 0

while True:
    if not video_capture.isOpened():
        print("unable to open camera")
        sleep(5)
        pass
    
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
    )

    for(x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    if anterior != len(faces):
        anterior = len(faces)
        print("faces: " + str(len(faces)));
    
    cv2.imshow('Video', frame)
    
    if cv2.waitKey(1) & 0xff == ord('q'):
        break


video_capture.release()
cv2.destroyAllWindows()
