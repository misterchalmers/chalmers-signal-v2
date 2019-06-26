import cv2 as cv
import numpy as np
import imutils
from imutils.video import VideoStream
import time


## foreground/background subtraction
# fgbg = cv.bgsegm.createBackgroundSubtractorMOG()
# fgbg = cv.createBackgroundSubtractorMOG2()
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(3,3))
fgbg = cv.bgsegm.createBackgroundSubtractorGMG()

## binary image black/white threshold
threshold = 110

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream("rtsp://192.168.8.3:8554/unicast").start()
time.sleep(2.0)
def main():
   # cam = cv.VideoCapture(0)

   while True:
       # ret, img = cam.read()
       frame = vs.read()
       frame = imutils.resize(frame, width=900)

       # convert cam feed to black and white
       # not necessary for wyzecam, it's nightvision
       # is already black and white
       # img_bw = cv.cvtColor(blob, cv.COLOR_BGR2GRAY)
       img_binary = cv.threshold(frame, threshold, 255, cv.THRESH_BINARY)[1]
       # apply foreground mask
       fgmask = fgbg.apply(img_binary)
       # not sure what this thing does
       fgmask_postMorphology = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel)

       cv.imshow('binary', img_binary)
       # cv.imshow('black/white', img_bw)
       # cv.imshow('fgmask', fgmask)
       cv.imshow('fgmask_postMorphology', fgmask_postMorphology)
       # cv.imshow('webcam', img)
       if cv.waitKey(1) == 27:
           break # esc to quit
   vs.release()
   cv.destroyAllWindows()
main()
