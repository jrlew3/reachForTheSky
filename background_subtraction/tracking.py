import cv2
import sys


faceCascade = cv2.CascadeClassifier("../data/haarcascades/haarcascade_frontalface_alt.xml")

def detectFace():
    while(1):
        print("Detecting face")
        ok, frame = video.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30,30),
        )
        
        maxArea = 0
        xpos = 0
        ypos = 0 
        width = 0
        height = 0

        # Send largest face
        for (x,y,w, h) in faces:
            if w*h > maxArea:
                xpos = int(x)
                ypos = int(y)
                width = int(w)
                hieght = int(h)
                maxArea = w*h

        if maxArea > 0:
            bbox = (x, y, w, h)
            return (frame, bbox) 

         

# BEGINNING OF MAIN 

# Initialize tracker 
trackingFace = 0 # Does not track face to begin with 
tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
tracker_type = tracker_types[6]

if tracker_type == 'MOSSE':
    tracker = cv2.TrackerMOSSE_create()

# Set up display
video = cv2.VideoCapture(0)

while True:
    # Initialize tracker 
    if not trackingFace:
        (frame, bbox) = detectFace()
        ok = tracker.init(frame, bbox)
        trackingFace = 1

    # Read frame
    ok, frame = video.read()
    if not ok:
        break

    ok, bbox = tracker.update(frame)
    
    if ok:
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255,0,0),2,1)
    else:
        trackingFace = 0
        break 

    cv2.imshow("Tracking", frame)

    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

