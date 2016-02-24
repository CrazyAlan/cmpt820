import numpy as np
import cv2
from MotionVec import *
from IntegerTransform import *
from ImageTransform import *
from FrameHandleHelpers import *
from IFrameHandle import *
from collections import deque
from BFrameHandle import *
#frames = []
QP = 0
cycleCount = 0
disCount = 0
CONSTANT_VIDEO_PATH = "SampleVideo_360x240_50mb.mp4"
cap = cv2.VideoCapture(CONSTANT_VIDEO_PATH)

IMT = ImageTransform()
IT = IntegerTransform()
IT.QuantizationMatrix(0)


ret, Frame = cap.read()
FRameBuffer = deque()
BFrameBuffer = deque()
FRameBuffer.append(Frame)
FRameBuffer.append(Frame)
BFrameBuffer.append(Frame)
BFrameBuffer.append(Frame)

FrameDecode = [] #Decoded Frame
DisplayFrame = [Frame, Frame, Frame]#Initialize 

PHand = PFrameHandle(QP)
IHand = IFrameHandle(QP)
BHand = BFrameHandle(QP)


'''
Displaying Sequence: I B B P B B P B B I  
Coding Sequence I P B B P B B I B B 
'''

while True:
    ret, Frame = cap.read()

    if cycleCount%9 == 0: #IFrame 
        IFrame = IMT.im2double(Frame)
        FrameDecode = IHand.IFrameDecoded(IFrame)

        FRameBuffer.popleft() #Pop out first buffer
        FRameBuffer.append(FrameDecode)  #Enque I frame

        DisplayFrame[0] = FrameDecode #Show at first
        #Decode BFrame
        IFrameRef = FRameBuffer.popleft()
        PFrameRef = FRameBuffer.popleft()
        FRameBuffer.append(PFrameRef) #Add back a frame
        for x in xrange(2):
            BFrame = BFrameBuffer.popleft()
            diffAndMotion = BHand.encode3Channels(IFrameRef, PFrameRef, BFrame)
            rgbImage = BHand.decode3Channels(IFrameRef, PFrameRef, diffAndMotion)
            DisplayFrame[x+1] = rgbImage #Add Frames into display

    elif cycleCount%3 == 0:  #PFrame
        PFrame = IMT.im2double(Frame)
       
        IRefFrame = FRameBuffer.popleft()

        diffAndMotion = PHand.encode3Channels(IRefFrame, PFrame)
        FrameDecode = PHand.decode3Channels(IRefFrame, diffAndMotion)

        #FRameBuffer.popleft() #Pop out first buffer
        FRameBuffer.append(FrameDecode)

        DisplayFrame[2] = FrameDecode #Show at first
        #Decode BFrame
        IFrameRef = FRameBuffer.popleft()
        PFrameRef = FRameBuffer.popleft()
        FRameBuffer.append(PFrameRef) #Add back a frame
        for x in xrange(2):
            BFrame = BFrameBuffer.popleft()
            diffAndMotion = BHand.encode3Channels(IFrameRef, PFrameRef, BFrame)
            rgbImage = BHand.decode3Channels(IFrameRef, PFrameRef, diffAndMotion)
            DisplayFrame[x] = rgbImage #Add Frames into display

        #Decode BFrame
    else: #BFrame
        BFrame = IMT.im2double(Frame) 
        BFrameBuffer.append(BFrame) #Every Time, append to buffer

    cv2.imshow('frame',Frame)

    cv2.imshow('frameDecode',DisplayFrame[disCount%3])
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cycleCount += 1 #Increase Cycle
    disCount += 1

cap.release()
cv2.destroyAllWindows()


