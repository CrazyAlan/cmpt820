import numpy as np
import cv2
from MotionVec import *
from IntegerTransform import *
from ImageTransform import *
from FrameHandleHelpers import *
from IFrameHandle import *
from collections import deque

#frames = []
QP = 0
cycleCount = 0
CONSTANT_VIDEO_PATH = "SampleVideo_360x240_50mb.mp4"
cap = cv2.VideoCapture(CONSTANT_VIDEO_PATH)

IMT = ImageTransform()
IT = IntegerTransform()
IT.QuantizationMatrix(0)

FRameBuffer = deque()


FrameDecode = [] #Decoded Frame
BFrameBuffer = []
DisplayFrame = []#Initialize 

PHand = PFrameHandle(QP)
IHand = IFrameHandle(QP)
BHand = BFrameHandle(QP)


'''
Displaying Sequence: I P P I P P I P P  
Coding Sequence I P B B P B B I B B 
'''

while True:
    ret, Frame = cap.read()

    if cycleCount%9 == 0: #IFrame 
        IFrame = IMT.im2double(Frame)
        FrameDecode = IHand.IFrameDecoded(IFrame)

        FRameBuffer = FrameDecode
    elif cycleCount%3 == 0:  #PFrame
        PFrame = IMT.im2double(Frame)
        diffAndMotion = PHand.encode3Channels(FRameBuffer, PFrame)
        FrameDecode = PHand.decode3Channels(FRameBuffer, diffAndMotion)

        FRameBuffer = FrameDecode

    else: #BFrame
        BFrameBuffer

    cv2.imshow('frame',Frame)
    cv2.imshow('frameDecode',FrameDecode)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cycleCount += 1 #Increase Cycle


cap.release()
cv2.destroyAllWindows()


