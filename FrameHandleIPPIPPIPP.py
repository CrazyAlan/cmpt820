import numpy as np
import cv2
from MotionVec import *
from IntegerTransform import *
from ImageTransform import *
from FrameHandleHelpers import *
from IFrameHandle import *

#frames = []
QP = 0
cycleCount = 0
CONSTANT_VIDEO_PATH = "SampleVideo_360x240_50mb.mp4"
cap = cv2.VideoCapture(CONSTANT_VIDEO_PATH)

IMT = ImageTransform()
IT = IntegerTransform()
IT.QuantizationMatrix(0)

FRameBuffer = []
Frame = []
FrameDecode = []

PHand = PFrameHandle(QP)
IHand = IFrameHandle(QP)



'''
Displaying Sequence: I P P I P P I P P  
Coding Sequence I P B B P B B I B B 
'''

while True:
    if cycleCount%3 == 0: #IFrame
        ret, Frame = cap.read()
        IFrame = IMT.im2double(Frame)
        FrameDecode = IHand.IFrameDecoded(IFrame)
        FRameBuffer = FrameDecode
    else:  #PFrame
        ret, Frame = cap.read()
        PFrame = IMT.im2double(Frame)
        diffAndMotion = PHand.encode3Channels(FRameBuffer, PFrame)
        rgbImage = PHand.decode3Channels(FRameBuffer, diffAndMotion)
        FrameDecode = rgbImage
        FRameBuffer = FrameDecode

    cv2.imshow('frame',Frame)
    cv2.imshow('frameDecode',FrameDecode)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cycleCount += 1
#diffAndMotion = PHand.encode3Channels(IFrame, PFrame)

#rgbImage = PHand.decode3Channels(IFrame, diffAndMotion)




cap.release()
cv2.destroyAllWindows()


    

#   if cv2.waitKey(1) & 0xFF == ord('q'):
#       break
