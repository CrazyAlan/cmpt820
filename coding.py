import quantization as quant
import numpy as np
import ImageTransform as imt
import dct 


def encode(imgRGB, quantMat):
	orgImage = imt.ImageTransform()
	orgImage.initFromRGB(imgRGB)
	#orgImage.showImage()

	'''yuv transform'''


	yuvImage = orgImage.rgb2yuv()
	#print yuvImage[:,:,0]
	#rgbImage = orgImage.yuv2rgb()

	#print (rgbImage.dtype)
	#orgImage.rgb2img(imgRGB).show()

	#rgbImage = orgImage.yuv2rgb()
	#rgbImage = rgbImage.astype(np.uint8)

	#print orgRGB - rgbImage
	#imgtoshow = orgImage.rgb2img(orgRGB - rgbImage)
	#imgtoshow.show()

	#print rgbImage
	'''sub sample'''
	orgImage.chromaSub() 


	#print orgImage.Y.shape
	#print orgImage.Cr.shape
	#print orgImage.Cb.shape

	'''vectorize all three channels'''
	vecY = dct.DCT.vecMat(orgImage.Y)
	vecCr = dct.DCT.vecMat(orgImage.Cr)
	vecCb = dct.DCT.vecMat(orgImage.Cb)

	#print np.shape(vecY)
	#print np.shape(vecCr)

	'''do DCT on YUV'''
	dctIm = dct.DCT()
	F_vecY = dctIm.dctVec(vecY)
	F_vecCr = dctIm.dctVec(vecCr)
	F_vecCb = dctIm.dctVec(vecCb)


	'''Quantization on all F'''
	imgQuant = quant.Quantization()
	imgQuant.initQTMatrix(quantMat)

	#print imgQuant.QuantMatrix.dtype
	F_vecY_Quan = imgQuant.quanitzeVec(F_vecY)
	F_vecCr_Quan = imgQuant.quanitzeVec(F_vecCr)
	F_vecCb_Quan = imgQuant.quanitzeVec(F_vecCb)
	
	#print np.min((F_vecY_Quan))
	F_info =  [F_vecY_Quan, F_vecCr_Quan, F_vecCb_Quan]
	orgShape = np.shape(imgRGB)
	return F_info, orgShape

def decode(F_info, quantMat, orgShape): #orgShape, orginal image shape
	'''Dequantization on all F'''
	imgQuant = quant.Quantization()
	imgQuant.initQTMatrix(quantMat)

	FRec_vecY_Quan = imgQuant.dquanitzeVec(F_info[0])
	FRec_vecCr_Quan = imgQuant.dquanitzeVec(F_info[1])
	FRec_vecCb_Quan = imgQuant.dquanitzeVec(F_info[2])

	'''IDCT'''
	dctIm = dct.DCT()
	f_vecY = dctIm.idctVec(FRec_vecY_Quan)
	f_vecCr = dctIm.idctVec(FRec_vecCr_Quan)
	f_vecCb = dctIm.idctVec(FRec_vecCb_Quan)

	recoverImg = imt.ImageTransform()
	recoverImg.initEmptyImage(orgShape) #initialize the same size image

	recoverImg.Y = dct.DCT.dvecMat(orgShape[0:2], f_vecY)
	recoverImg.Cr = dct.DCT.dvecMat(np.array(orgShape[0:2])/2, f_vecCr)
	recoverImg.Cb = dct.DCT.dvecMat(np.array(orgShape[0:2])/2, f_vecCb) 

	recoverImg.chromaExpand()

	#print np.sum(recoverImg.Y - orgImage.Y)
	#print np.sum(recoverImg.yuv[:,:,0] - orgImage.yuv[:,:,0])


	recRGBImg = recoverImg.yuv2rgb()
	recRGBImg = recRGBImg.astype(np.uint8)

	#print (imageRGB)
	imgtoshow = recoverImg.rgb2img(recRGBImg)
	#imgtoshow.show()
	return recRGBImg, imgtoshow
	