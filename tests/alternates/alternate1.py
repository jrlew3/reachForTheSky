import numpy as np
import cv2

# Capture video frames
cap = cv2.VideoCapture(0)
# https://docs.opencv.org/3.4/db/d5c/tutorial_py_bg_subtraction.html
# history, threshold, detect shadows.
fgbg = cv2.createBackgroundSubtractorMOG2(600, 30, False)


screenw, screenh = 1279, 719

initW, initH = 200, 200
initX, initY = screenw - initW, 100
begin = True
# non active state to begin with
neutral = True
dir1 = "l"
upDown = "0" # value can be "0", "u", or "d"
timer = 0
activeCounter = 0

def getImageRegion(canvas, x, y, initW, initH):
    top = canvas[ (x+ initW//4) : (x + (initW//4)*3) , y : (y + initH//4) ]
    bot = canvas[ (x+ initW//4) : (x + (initW//4)*3) , (y + (initH//4)*3) : (y + initH) ]
    right = canvas[ (x+ (initW//4)*3) : (x+initW), (y + initH//4) : (y + (initH//4)*3) ]
    left = canvas[ x : (x + initW//4) , (y + initH//4) : (y + (initH//4)*3)]
    topR = canvas[ (x+ (initW//4)*3) : (x+initW), y : (y + initH//4)]
    topL = canvas[ x : (x + initW//4), y : (y + initH//4)]
    botR = canvas[ (x+ (initW//4)*3) : (x + initW), (y + (initH//4)*3) : (y + initH) ]
    botL = canvas[ x : (x + initW//4), (y + (initH//4)*3) : (y + initH)]
    return top, bot, right, left, topR, topL, botR, botL

# if there are lots of pixels in cloud region, returns stuff.  else return false.
def isCloudTouch(canvas, x1, y1, x2, y2):
    input_img = canvas[x1:x2, y1:y2]
    whitecoord = np.argwhere(input_img == 255)

    # print("whitecoord", whitecoord)

    if not whitecoord.any():
        print("NO WHITE PIXELS")
        print("whitecoord", whitecoord)
        return False

    elif whitecoord.any(): #white pixel in cloud
        print("WHITE PIXELS")
        print("whitecoord", whitecoord)
        return True


# returns more specific values of the regions being touched in cloud.
# http://answers.opencv.org/question/98980/how-to-retrieve-all-coordinates-of-pixels-of-specific-colour-in-an-image/
def cloudTouchRegions(canvas, x, y):
    [top, bot, right, left, topR, topL, botR, botL] = getImageRegion(canvas, x, y, initW, initH)
    dlist = [top, bot, right, left, topR, topL, botR, botL]
    thingList = ["top", "bot", "right", "left", "topR", "topL", "botR", "botL"]
    regions = []
    count = 0
    for thing in dlist:
        if (np.argwhere(thing == 255)).any:
            regions.append(thingList[count])
        count += 1
    return regions


# for one cloud, so far.  Neutral state is just back and forth.
def neutralState(x, y, dir):
    #why isn't this working...
    if x < 100:
        dir == "r"

    elif dir == "r" and x > screenw - initW:
        dir = "l"

    if dir == "r":
        x += 5
    elif dir == "l":
        x -= 5
    print(x, y, dir)
    return x, y, dir

def activeState(x, y, upDownDir):
    # currently works only in up/down position

    if upDownDir == "up":
        y += 10
    elif upDownDir == "down":
        y -= 10
    print(x, y, upDownDir)
    return x, y, upDownDir

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(frame, (5,5),0)
    fgmask = fgbg.apply(frame)

    kernel = np.ones((6,6), np.uint8)
    # erosion = cv2.erode(fgmask, kernel, iterations=1)
    # dilation = cv2.dilate(fgmask, kernel, iterations=1)
    opening = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    # initializes cloud position
    if begin:
        (x, y) = (initX, initY)
        (w, h) = (initW, initH)
        begin = False

    cv2.rectangle(opening, (x, y), (x+w, y+h), (255, 0, 0), 10)

    # check if cloud is being touched.  If so, find region of cloud that is being touched.  give UpDowndir a direciton.
    if isCloudTouch(opening, x, y, x+w, y+h):
        print("CLOUD IS TOUCHED")
        neutral = False
        regionsTouched = cloudTouchRegions(opening, x, y)
        print(regionsTouched)
        if "top" in regionsTouched:
            upDown = "down"
        elif "bot" in regionsTouched:
            upDown = "up"

    if neutral:
        (x, y, dir1) = neutralState(x, y, dir1)
        print("here", x, y, dir1)

    # if cloud touched, move the cloud for a bit with function, then go back to neutral state.
    elif not neutral:
        (x, y, upDown) = activeState(x, y, upDown)
        activeCounter += 1
        if activeCounter > 10:
            neutral = True
            upDown = "0"
            activeCounter = 0

    ######## cv2.imshow('frame', fgmask)
    cv2.imshow('opening', opening)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
