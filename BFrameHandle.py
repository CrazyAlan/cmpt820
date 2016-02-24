import numpy as np
import cv2
from MotionVec import *
from IntegerTransform import *
from ImageTransform import *


'''
Encode: 
	Input: Reference IFrame and PFrame, B Frame
	Output: two MotionVector, min mad,  IntegerTransformed Difference Frame
Decode:
	Input: Reference IFrame and PFrame, difference Image,  two MotionVector, min mad,
'''

class BFrameHandle():
	def __init__(self, QP):
		self.data = []
		self.IMT = ImageTransform()
		self.IT = IntegerTransform()
		self.IT.QuantizationMatrix(QP)

	def encode3Channels(self, IFrame, PFrame, BFrame):
		yuvI = self.IMT.rgb2yuv(IFrame)
		yuvP = self.IMT.rgb2yuv(PFrame)
		yuvB = self.IMT.rgb2yuv(BFrame)

		[Y_I, Cr_I, Cb_I] = self.IMT.chromaSub(yuvI)
		[Y_P, Cr_P, Cb_P] = self.IMT.chromaSub(yuvP)
		[Y_B, Cr_B, Cb_B] = self.IMT.chromaSub(yuvB)

		[diffY, motionInfoY] = self.encode(Y_I,Y_P,Y_B)
		[diffCr, motionInfoCr] = self.encode(Cr_I,Cr_P,Cr_B)
		[diffCb, motionInfoCb] = self.encode(Cb_I,Cb_P,Cb_B)

		return [diffY, motionInfoY, diffCr, motionInfoCr, diffCb, motionInfoCb]
	
	def encode(self, IFrame, PFrame, BFrame):
		mvB = MotionVecB(IFrame, PFrame, BFrame) #Initialize A instance
		#[motionVect1, minMad1, motionVect2, minMad2]
		motionInfo = mvB.getTwoMotionVector()

		estimatedBFrame = mvB.recoverPfromI(IFrame, PFrame, motionInfo)
		diffEstMinusReal = BFrame - estimatedBFrame 

		# Integer Transfer		
		diffEstMinusRealVec = self.IMT.vecMat(diffEstMinusReal, 4)
		diffEstMinusRealVecIntTran = self.IT.EnIntegerTransformVec(diffEstMinusRealVec)

		return [diffEstMinusRealVecIntTran, motionInfo]

	def decode3Channels(self, IFrame, PFrame, diffAndmotionVector):
		yuvI = self.IMT.rgb2yuv(IFrame)
		yuvP = self.IMT.rgb2yuv(PFrame)

		[Y_I, Cr_I, Cb_I] = self.IMT.chromaSub(yuvI)
		[Y_P, Cr_P, Cb_P] = self.IMT.chromaSub(yuvP)

		[diffY, motionInfoY, diffCr, motionInfoCr, diffCb, motionInfoCb] = diffAndmotionVector		

		Y_B = self.decode(Y_I, Y_P, diffY, motionInfoY)
		Cr_B = self.decode(Cr_I, Cr_P, diffCr, motionInfoCr)
		Cb_B = self.decode(Cb_I, Cb_P, diffCb, motionInfoCb)

		#Expand all 3 channels
		yuvRec = self.IMT.chromaExpand(Y_B, Cr_B, Cb_B)
		rgbImRec = self.IMT.yuv2rgb(yuvRec)
		rgbIm =  self.IMT.double2uintImage(rgbImRec)

		return rgbIm


	def decode(self, IFrame, PFrame, diff,  motionInfo):
		mvB = MotionVecB(IFrame, PFrame, np.zeros_like(IFrame)) #Here use both I frame to initialize, as no need for Pframe
		estimatedBFrame = mvB.recoverPfromI(IFrame, PFrame, motionInfo)
		
		#DeInteger Transform for diff
		diffDetraned = self.IT.DeIntegerTransformVec(diff)
		diffRec = self.IMT.dvecMat(np.shape(IFrame), diffDetraned, 4)

		PFrame = estimatedBFrame + diffRec


		return PFrame

if __name__ == '__main__':
	frames = []

	for i in xrange(30,40):
	    tmpFrame = cv2.imread("Frames/singleFrame"+str(i)+".tif")
	   # cv2.imshow('image', tmpFrame)
	    frames.append(tmpFrame)

	IMT = ImageTransform()
	

	'''
	Displaying Sequence: I B B P B B P B B I 
	Coding Sequence I P B B P B B I B B 
	'''
	#for i in range(1): #10 frames handle
		
		#Read Image Frames as double
		#rgbIm1 = IMT.im2double(frames[i])
	IFrame = IMT.im2double(frames[5])
	BFrame = IMT.im2double(frames[6])
	PFrame = IMT.im2double(frames[7])

	BHand = BFrameHandle(0)
	diffAndMotion = BHand.encode3Channels(IFrame, PFrame, BFrame)

	rgbImage = BHand.decode3Channels(IFrame, PFrame, diffAndMotion)

	print(np.sum(rgbImage-PFrame))
	cv2.imshow('image1', IMT.double2uintImage(BFrame))
	cv2.imshow('image2', IMT.double2uintImage(rgbImage))

	#cv2.imshow('image', IMT.double2uintImage(PFrame))

	cv2.waitKey(0)
	cv2.destroyAllWindows()