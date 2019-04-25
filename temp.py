import datetime
import math
import cv2
import numpy as np
import time
import imutils
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
#GPIO library for buttons
# display libraries
# import Adafruit_GPIO.SPI as SPI
# import Adafruit_SSD1306
# from PIL import Image
# from PIL import ImageDraw
# from PIL import ImageFont
#
# #declare and instantiate display
# RST = None
# DC = 23
# SPI_PORT = 0
# SPI_DEVICE = 0
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

#global variables
width = 0
height = 0
EntranceCounter = 0
ExitCounter = 0
MinCountourArea = 550  #Adjust ths value according to your usage
BinarizationThreshold = 55  #Adjust ths value according to your usage
OffsetRefLines = 75  #Adjust ths value according to your usage

#Check if an object is entering in monitored zone
def CheckEntranceLineCrossing(y, CoorYEntranceLine, CoorYExitLine):
    AbsDistance = abs(y - CoorYEntranceLine)
    if ((AbsDistance <= 2) and (y < CoorYExitLine)):
        return 1
    else:
        return 0

#Check if an object in exitting from monitored zone
def CheckExitLineCrossing(y, CoorYEntranceLine, CoorYExitLine):
    AbsDistance = abs(y - CoorYExitLine)
    if ((AbsDistance <= 2) and (y > CoorYEntranceLine)):
        return 1
    else:
        return 0

#initialize the Camera
##force 640x480 webcam resolution



vs = VideoStream("rtsp://192.168.8.213:8554/unicast").start()
time.sleep(2.0)

# allow the camera to warmup
time.sleep(0.1)

W = 640
H = 480

#camera.set(3,640)
#camera.set(4,480)
# grab an image from the camera
ReferenceFrame = None

# capture frames from the camera
#for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=720)
	# grab the raw NumPy array representing the image
    image = frame
   # vs = frame.array
#    height = np.size(vs,0)
#    width = np.size(vs,1)
    GrayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    GrayFrame = cv2.GaussianBlur(GrayFrame, (21, 21), 0)

    if ReferenceFrame is None:
        ReferenceFrame = GrayFrame
        #continue

    #Background subtraction and image binarization
    FrameDelta = cv2.absdiff(ReferenceFrame, GrayFrame)
    FrameThresh = cv2.threshold(FrameDelta, BinarizationThreshold, 255, cv2.THRESH_BINARY)[1]

#    #Background subtraction and image binarization
    FrameThresh = cv2.dilate(FrameThresh, None, iterations=3)
    #cnts = cv2.findContours(FrameThresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    major = cv2.__version__.split('.')[0]
    if major == '3':
        _, contours, _ = cv2.findContours(FrameThresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        contours, _ = cv2.findContours(FrameThresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)#
    QttyOfContours = 0
#
#    #plot reference lines (entrance and exit lines)
    CoorYEntranceLine = 220#(height / 2)-OffsetRefLines
    CoorYExitLine = 520#(height / 2)+OffsetRefLines
    cv2.line(image, (220, 0), (220, H), (0,0,255), 5)#blue entrance
    cv2.line(image, (520, 0), (520, H), (255,0,0), 5)#red exit

 #   cv2.line(image, (0,CoorYEntranceLine), (width,CoorYEntranceLine), (255, 0, 0), 2)
 #   cv2.line(image, (0,CoorYExitLine), (width,CoorYExitLine), (0, 0, 255), 2)
    for c in contours:
        #if a contour has small area, it'll be ignored
        if cv2.contourArea(c) < MinCountourArea:
            continue
        QttyOfContours = QttyOfContours+1

        #draw an rectangle "around" the object
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        #find object's centroid
        CoordXCentroid = int((x+x+w)/2)
        CoordYCentroid = int((y+y+h)/2)
        ObjectCentroid = (CoordXCentroid,CoordYCentroid)
        #print ObjectCentroid
        cv2.circle(frame, ObjectCentroid, 1, (0, 0, 0), 5)
#        if CoordXCentroid > 220:
#            ExitCounter += 1

        if (CheckEntranceLineCrossing(CoordXCentroid,320,420)):
            EntranceCounter += 1
        if (CheckEntranceLineCrossing(CoordXCentroid,420,320)):
            ExitCounter += 1

       # print "Total countours found: "+str(QttyOfContours)
    #
#    #Write entrance and exit counter values on frame and shows it
    cv2.putText(image, "Entrances: {}".format(str(EntranceCounter)), (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 0, 1), 2)
    cv2.putText(image, "Exits: {}".format(str(ExitCounter)), (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
#    cv2.imshow("Original Frame", frame)


	# show the frame
    cv2.imshow("Frame", image)
    # cv2.imshow("Thresh", FrameThresh)
    key = cv2.waitKey(1) & 0xFF
 	# clear the stream in preparation for the next frame
 #   rawCapture.truncate(0)
    # grab the raw NumPy array representing the image
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        #camera.close()
        cv2.destroyAllWindows()
        vs.stop()
        cv2.destroyAllWindows()
        break
cv2.destroyAllWindows()
vs.stop()