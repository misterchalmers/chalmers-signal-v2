import cv2 as cv
import numpy as np

## foreground/background subtraction
# fgbg = cv.bgsegm.createBackgroundSubtractorMOG()
# fgbg = cv.createBackgroundSubtractorMOG2()
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(3,3))
fgbg = cv.bgsegm.createBackgroundSubtractorGMG()

## binary image black/white threshold
threshold = 110

def main():
   cam = cv.VideoCapture(0)
   while True:
       ret, img = cam.read()

       # convert cam feed to black and white
       img_bw = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
       img_binary = cv.threshold(img_bw, threshold, 255, cv.THRESH_BINARY)[1]
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
   cam.release()
   cv.destroyAllWindows()
main()
