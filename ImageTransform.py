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
		

	def readImage(self, path):
		self.img = Image.open(path)
		self.rgb = np.array(self.img)
		return self.rgb

	def showImage(self):
		self.img.show()

	def rgb2yuv(self):
		self.yuv = (self.rgb).dot(np.transpose(self.rgb2yuvMat))
		return self.yuv
	def yuv2rgb(self):
		self.rgb = (self.yuv).dot(np.transpose(self.yuv2rgbMat))
		#print self.rgb
		self.rgb[self.rgb<0] = 0
		self.rgb[self.rgb>255] = 255
		#print np.max(self.rgb)
		#print np.min(self.rgb)

		self.rgb = self.rgb.astype(np.uint8)
	  	return self.rgb

	def chromaSub(self):
		self.Y = self.yuv[:,:,0]
		self.Cr = self.yuv[:,:,1]
		self.Cb = self.yuv[:,:,2]
		#self.Cr = self.yuv[0::2, 0::2, 1] #seems wrong on book
		#self.Cb = self.yuv[0::2, 0::2, 2]

	def chromaExpand(self):
		self.yuv[:,:,0] = self.Y
		self.yuv[:,:,1] = self.Cr
		self.yuv[:,:,2] = self.Cb

		#self.yuv[:,:,1] = np.repeat(np.repeat(self.Cr,2, axis=0), 2, axis=1)
		#self.yuv[:,:,2] = np.repeat(np.repeat(self.Cb,2, axis=0), 2, axis=1)

	def rgb2img(self, rgb):	
		img = Image.fromarray(rgb)
		return img

	@staticmethod
	def imresize(orgImgObj, shapeInfo, ratio):
		outImg = orgImgObj.resize((np.array(shapeInfo[1])/ratio, np.array(shapeInfo[0])/ratio))
		return outImg


'''
newImage = ImageTransform()
orgrgb = newImage.readImage("kodim23.png")
newImage.showImage()
'''



