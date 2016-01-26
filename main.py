import quantization as quant
import numpy as np
import ImageTransform as imt
import dct 


orgImage = imt.ImageTransform()
orgRGB = orgImage.readImage("kodim23.png")
#orgImage.showImage()

'''yuv transform'''
yuvImage = orgImage.rgb2yuv()
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
'''imgQuant = quant.Quantization()
quantMat = np.full([8,8], 1)
imgQuant.initQTMatrix(quantMat)

F_vecY_Quan = imgQuant.quanitzeVec(F_vecY)
F_vecCr_Quan = imgQuant.quanitzeVec(F_vecCr)
F_vecCb_Quan = imgQuant.quanitzeVec(F_vecCb)
'''

'''Dequantization'''
'''FRec_vecY_Quan = imgQuant.dquanitzeVec(F_vecY_Quan)
FRec_vecCr_Quan = imgQuant.dquanitzeVec(F_vecCr_Quan)
FRec_vecCb_Quan = imgQuant.dquanitzeVec(F_vecCb_Quan)
'''

f_vecY = dctIm.idctVec(F_vecY)
f_vecCr = dctIm.idctVec(F_vecCr)
f_vecCb = dctIm.idctVec(F_vecCb)


recoverImg = imt.ImageTransform()
recoverImg.initEmptyImage(orgRGB) #initialize the same size image

recoverImg.Y = dct.DCT.dvecMat(orgImage.Y, f_vecY)
recoverImg.Cr = dct.DCT.dvecMat(orgImage.Cr, f_vecCr)
recoverImg.Cb = dct.DCT.dvecMat(orgImage.Cb, f_vecCb) 


print np.sum(recoverImg.Y - orgImage.Y)

recoverImg.chromaExpand()

recRGBImg = recoverImg.yuv2rgb()
recRGBImg = recRGBImg.astype(np.uint8)



#print (imageRGB)
imgtoshow = recoverImg.rgb2img(recRGBImg)
imgtoshow.show()

