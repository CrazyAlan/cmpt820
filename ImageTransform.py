from PIL import Image

import numpy as np



class ImageTransform:
	"""docstring for ImageTransform"""
	def __init__(self):
		self.rgb2yuvMat = np.array([[0.299,0.587,0.114], [-0.14713, -0.28886, 0.436], [0.615, -0.51499, -0.10001]])
		self.yuv2rgbMat = np.array([[1, 0, 1.13983],[1, -0.39465, -0.58060],[1, 2.03211, 0]])

	def initEmptyImage(self, shapeInfo):
		self.rgb = np.zeros(shapeInfo, dtype=np.float64)
		self.yuv = np.zeros(shapeInfo, dtype=np.float64)
		#self.img = self.rgb2img(self.rgb)
	def initFromRGB(self, rgbImg):
		self.rgb = rgbImg
		self.img = self.rgb2img(rgbImg)
		
	def im2double(self, rgbImg):
		doubleRGBImage = rgbImg.astype(np.float32)
		return doubleRGBImage
	def double2uintImage(self, doubleImg):
		minValue = np.amin(doubleImg)
		if minValue < 0:
			doubleImg += abs(minValue)
		maxValue = np.amax(doubleImg)
		doubleImg /= maxValue
		doubleImg *= 255
		uintImage = doubleImg.astype(np.uint8)
		return uintImage

	def readImage(self, path):
		self.img = Image.open(path)
		self.rgb = np.array(self.img)
		return self.rgb

	def showImage(self):
		self.img.show()

	def rgb2yuv(self, rgb):
		yuv = (rgb).dot(np.transpose(self.rgb2yuvMat))
		return yuv

	def yuv2rgb(self, yuv):
		rgb = (yuv).dot(np.transpose(self.yuv2rgbMat))
	
	  	return rgb

	def chromaSub(self, yuv):
		Y = yuv[:,:,0]
		Cr = yuv[0::2, 0::2, 1] #seems wrong on book
		Cb = yuv[0::2, 0::2, 2]
		return [Y, Cr, Cb]

	def chromaExpand(self, Y, Cr, Cb):
		[rows, cols] = np.shape(Y)
		yuv = np.zeros([rows, cols, 3])
		yuv[:,:,0] = Y
		yuv[:,:,1] = np.repeat(np.repeat(Cr,2, axis=0), 2, axis=1)
		yuv[:,:,2] = np.repeat(np.repeat(Cb,2, axis=0), 2, axis=1)

		return yuv

	def rgb2img(self, rgb):	
		img = Image.fromarray(rgb)
		return img

	#vectorize the matrix
	def vecMat(self, inMat, bSize):
		[rows, cols] = np.shape(inMat)
		outMat = np.empty([rows*cols/(bSize*bSize), bSize, bSize])
		for i in xrange(0, rows/bSize):
			for j in xrange(0, cols/bSize):
				outMat[i*cols/bSize + j,:,:] =  inMat[i*bSize:i*bSize+bSize,j*bSize:j*bSize+bSize]
		return outMat

	#devectorize the matrix
	def dvecMat(self, shapeInfo, inMat, bSize):
		[rows, cols] = shapeInfo
		outMat = np.empty([rows, cols])
		for i in xrange(0, rows/bSize):
			for j in xrange(0, cols/bSize):
				outMat[i*bSize:i*bSize+bSize, j*bSize:j*bSize+bSize] = inMat[i*cols/bSize + j, :, :]
		return outMat




	@staticmethod
	def imresize(orgImgObj, shapeInfo, ratio):
		outImg = orgImgObj.resize((np.array(shapeInfo[1])/ratio, np.array(shapeInfo[0])/ratio))
		return outImg


'''
newImage = ImageTransform()
orgrgb = newImage.readImage("kodim23.png")
newImage.showImage()
'''



