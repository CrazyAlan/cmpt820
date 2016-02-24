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
QP = 8
cycleCount = 0
displayCount = 0

CONSTANT_VIDEO_PATH = "timedVideo.mp4"
cap = cv2.VideoCapture(CONSTANT_VIDEO_PATH)

IMT = ImageTransform()
IT = IntegerTransform()
IT.QuantizationMatrix(0)

ret, Frame = cap.read()


RefFrameBuffer = deque()
BFrameBuffer = deque()

FrameDecode = []

DisplayFrame = [Frame,Frame,Frame,Frame,Frame,Frame]

PHand = PFrameHandle(QP)
IHand = IFrameHandle(QP)
BHand = BFrameHandle(QP)


'''
Displaying Sequence: I P P I P P I P P  
Coding Sequence I P B B P B B I B B 
'''

framName = "I"

while True:

    ret, Frame = cap.read()

    if cycleCount%9 == 0: #IFrame
        IFrame = IMT.im2double(Frame)
        FrameDecode = IHand.IFrameDecoded(IFrame)
        print('I', (displayCount+3+2)%6)
        DisplayFrame[(displayCount+3+2)%6] = FrameDecode
        RefFrameBuffer.append(FrameDecode)
        #DisplayFrame[]
        framName = "I"

    elif cycleCount%3 == 0:  #PFrame
        PFrame = IMT.im2double(Frame)

        RefFrame = RefFrameBuffer.pop()
        RefFrameBuffer.append(RefFrame)

        diffAndMotion = PHand.encode3Channels(RefFrame, PFrame)
        rgbImage = PHand.decode3Channels(RefFrame, diffAndMotion)
        FrameDecode = rgbImage
        DisplayFrame[(displayCount+3+2)%6] = FrameDecode
        print('P', (displayCount+3+2)%6)
        RefFrameBuffer.append(FrameDecode)
        framName = "P"

    else: #BFrame
        BFrame = IMT.im2double(Frame) 
        BFrameBuffer.append(BFrame) #Every Time, append to buffer
        framName = "B"

    if cycleCount%3 == 0 and cycleCount>0: #IFrame or PFrame, Decode B Frame
        IFrameRef = RefFrameBuffer.popleft()
        PFrameRef = RefFrameBuffer.popleft()
        RefFrameBuffer.append(PFrameRef)

        #Encode and Decode
        for x in range(2):
            BFrame = BFrameBuffer.popleft()

            diffAndMotion = BHand.encode3Channels(IFrameRef, PFrameRef, BFrame)
            rgbImage = BHand.decode3Channels(IFrameRef, PFrameRef, diffAndMotion)
            print ('B', (displayCount+3+x)%6)
            DisplayFrame[(displayCount+3+x)%6] = rgbImage

    cv2.imshow('frameDecode',DisplayFrame[displayCount%6])
    cv2.imshow('frame',Frame)

    cv2.imwrite('Output/frame' +str(displayCount)+ '_'+framName + '.jpg', DisplayFrame[displayCount%6])
    print('Displaying', displayCount%6)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cycleCount += 1
    displayCount += 1
#diffAndMotion = PHand.encode3Channels(IFrame, PFrame)

#rgbImage = PHand.decode3Channels(IFrame, diffAndMotion)




cap.release()
cv2.destroyAllWindows()


    

#   if cv2.waitKey(1) & 0xFF == ord('q'):
#       break
