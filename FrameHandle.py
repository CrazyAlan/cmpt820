import numpy as np
import cv2
from MotionVec import *
from IntegerTransform import *
from ImageTransform import *
from FrameHandleHelpers import *

frames = []

for i in xrange(30,40):
    tmpFrame = cv2.imread("Frames/singleFrame"+str(i)+".tif")
   # cv2.imshow('image', tmpFrame)
    frames.append(tmpFrame)

IMT = ImageTransform()
IT = IntegerTransform()
IT.QuantizationMatrix(0)

'''
Displaying Sequence: I B B P B B P B B I 
Coding Sequence I P B B P B B I B B 
'''
#for i in range(1): #10 frames handle
	
	#Read Image Frames as double
	#rgbIm1 = IMT.im2double(frames[i])
IFrame = IMT.im2double(frames[3])
PFrame = IMT.im2double(frames[4])

PHand = PFrameHandle(100)
diffAndMotion = PHand.encode3Channels(IFrame, PFrame)

rgbImage = PHand.decode3Channels(IFrame, diffAndMotion)



print np.sum(abs(rgbImage - PFrame))
cv2.imshow('image1', IMT.double2uintImage(PFrame))

cv2.imshow('image2', IMT.double2uintImage(rgbImage))
cv2.waitKey(0)
cv2.destroyAllWindows()


	

#	if cv2.waitKey(1) & 0xFF == ord('q'):
#		break
