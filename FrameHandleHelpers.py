import numpy as np
import cv2
from MotionVec import *
from IntegerTransform import *
from ImageTransform import *



'''
Encode: 
	Input: Reference IFrame, PFrame
	Output: MotionVector, IntegerTransformed Difference Frame
Decode:
	Input: Reference IFrame, difference Image,  MotionVector
'''
class PFrameHandle():
	def __init__(self):
		self.data = []
		self.IMT = ImageTransform()

	def encode3Channels(self, IFrame, PFrame):
		yuvI = self.IMT.rgb2yuv(IFrame)
		yuvP = self.IMT.rgb2yuv(IFrame)

		[Y_I, Cr_I, Cb_I] = self.IMT.chromaSub(yuvI)
		[Y_P, Cr_P, Cb_P] = self.IMT.chromaSub(yuvP)

		[diffY, motionVectorY] = self.encode(Y_I,Y_P)
		[diffCr, motionVectorCr] = self.encode(Cr_I,Cr_P)
		[diffCb, motionVectorCb] = self.encode(Cb_I,Cb_P)

		return [diffY, motionVectorY, diffCr, motionVectorCr, diffCb, motionVectorCb]
	
	def encode(self, IFrame, PFrame):
		mvP = MotionVecP(IFrame, PFrame) #Initialize A instance
		motionVector = mvP.getMotionVecForAll()
		estimatedPFrame = mvP.recoverPfromI(IFrame, motionVector)
		diffEstAndReal = PFrame - estimatedPFrame 

		return [diffEstAndReal, motionVector]

	def decode3Channels(self, IFrame, diffAndmotionVector):

		[Y_I, Cr_I, Cb_I] = self.IMT.chromaSub(IFrame)
		[diffY, motionVectorY, diffCr, motionVectorCr, diffCb, motionVectorCb] = diffAndmotionVector		

		Y_P = self.decode(Y_I, diffY, motionVectorY)
		Cr_P = self.decode(Cr_I, diffCr, motionVectorCr)
		Cb_P = self.decode(Cb_I, diffCb, motionVectorCb)

		#Expand all 3 channels
		yuvRec = self.IMT.chromaExpand(Y_P, Cr_P, Cb_P)
		#rgbImRec = self.IMT.yuv2rgb(yuvRec)

		return yuvRec

	def decode(self, IFrame, diff,  motionVector):
		mvP = MotionVecP(IFrame, IFrame) #Here use both I frame to initialize, as no need for Pframe
		estimatedPFrame = mvP.recoverPfromI(IFrame, motionVector)
		PFrame = estimatedPFrame + diff

		return PFrame



class BFrameHandle():
	def __init__(self):
		self.data = []

class IFrameHandle():
	def __init__(self):
		self.data = []	



if __name__ == '__main__':
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

	PHand = PFrameHandle()
	diffAndMotion = PHand.encode3Channels(IFrame, PFrame)

	rgbImage = PHand.decode3Channels(IFrame, diffAndMotion)


	cv2.imshow('image', IMT.double2uintImage(rgbImage[:,:,:]))
	cv2.waitKey(0)
	cv2.destroyAllWindows()