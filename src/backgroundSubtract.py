import cv2 as cv
import numpy as np

fgbg = cv.bgsegm.createBackgroundSubtractorMOG()

def main():
   cam = cv.VideoCapture(0)
   while True:
       ret_val, img = cam.read()
       cv.imshow('webcam', img)
       if cv.waitKey(1) == 27:
           break # esc to quit
   cv.destroyAllWindows()
main()
