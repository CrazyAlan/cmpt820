'''
Input: RGB Image

Output: RGB Image

'''


import numpy as np
import cv2
from MotionVec import *
from IntegerTransform import *
from ImageTransform import *
from Intra4by4Coding import *

class IFrameHandle():
	def __init__(self, QP):
		self.data = []	
		self.IC = IntraCoding(QP)
		self.IMT = ImageTransform()
	def IFrameDecoded(self, IFrame):
		yuvI = self.IMT.rgb2yuv(IFrame)
		[Y_I, Cr_I, Cb_I] = self.IMT.chromaSub(yuvI)

		Y_rec = self.encode(Y_I)
		Cr_rec = self.encode(Cr_I)
		Cb_rec = self.encode(Cb_I)
		#print np.shape(Y_rec)
		yuvRec = self.IMT.chromaExpand(Y_rec, Cr_rec, Cb_rec)
		rgbImRec = self.IMT.yuv2rgb(yuvRec)
		rgbIm = self.IMT.double2uintImage(rgbImRec)

		return rgbIm

	def encode(self, IFrame):
		recFrame = self.IC.IntraCodingVec(IFrame)
		return recFrame

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
	

	IHand = IFrameHandle(40)
	
	rgbImage = IHand.IFrameDecoded(IFrame)

	print(np.sum(abs(rgbImage-IFrame)))
	cv2.imshow('image1', IMT.double2uintImage(IFrame))
	cv2.imshow('image2', IMT.double2uintImage(rgbImage))

	#cv2.imshow('image', IMT.double2uintImage(PFrame))

	cv2.waitKey(0)
	cv2.destroyAllWindows()