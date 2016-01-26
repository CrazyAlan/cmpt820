import coding 
import numpy as np
import scipy as sp
import quantization as quant
import ImageTransform as imt
import dct 


quantMat = np.full([8,8], 1)

#Read Image
orgImage = imt.ImageTransform()
orgRGB = orgImage.readImage("kodim23.png")

#Reduce resolution
imgPIL = orgImage.rgb2img(orgRGB)
halfImg = imt.ImageTransform.imresize(imgPIL, np.shape(orgRGB), 2)
quartImg = imt.ImageTransform.imresize(imgPIL, np.shape(orgRGB), 4)

'''Hierachical Encoding'''
#Encode quartImg
F_info_quart, orgShape_quart = coding.encode(np.array(quartImg), quantMat)
#Decode QuartImg
recRGB_quart, recImg2show_quart = coding.decode(F_info_quart, quantMat, orgShape_quart)
#recImg2show_quart.show()

#Encode half  Image



#tmp.show()
#recImg = quartImg.resize((np.shape(orgRGB)[1], np.shape(orgRGB)[0]))
#recImg.show()

