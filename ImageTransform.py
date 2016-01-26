from PIL import Image

import numpy as np



class ImageTransform:
	"""docstring for ImageTransform"""
	def __init__(self):
		self.rgb2yuvMat = np.array([[0.299,0.587,0.114], [-0.14713, -0.28886, 0.436], [0.615, -0.51499, -0.10001]])
		self.yuv2rgbMat = np.array([[1, 0, 1.13983],[1, -0.39465, -0.58060],[1, 2.03211, 0]])

	def initEmptyImage(self, imgRGB):
		self.rgb = np.zeros_like(imgRGB)
		self.yuv = np.zeros_like(imgRGB)
		self.img = self.rgb2img(self.rgb)

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
	  	return self.rgb

	def chromaSub(self):
		self.Y = self.yuv[:,:,0]
		self.Cr = self.yuv[0::2, 1::2, 1] #seems wrong on book
		self.Cb = self.yuv[0::2, 1::2, 2]

	def chromaExpand(self):
		self.yuv[:,:,0] = self.Y
		self.yuv[:,:,1] = np.repeat(np.repeat(self.Cr,2, axis=0), 2, axis=1)
		self.yuv[:,:,2] = np.repeat(np.repeat(self.Cb,2, axis=0), 2, axis=1)

	def rgb2img(self, rgb):	
		img = Image.fromarray(rgb)
		return img

'''
newImage = ImageTransform()
orgrgb = newImage.readImage("kodim23.png")
newImage.showImage()
'''



