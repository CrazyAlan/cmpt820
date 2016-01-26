import coding 
import numpy as np
import scipy as sp
import quantization as quant
import ImageTransform as imt
import dct 
import hierarchical as hr


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
#print orgShape_quart
#Decode QuartImg
recRGB_quart, recImg2show_quart = coding.decode(F_info_quart, quantMat, orgShape_quart)
#recImg2show_quart.show()

#Encode half diff  Image
hierVar = hr.Hier(quantMat)
halfdiffF_info, halfdifforgShape, hafldiffrecRGB, halfdiffrecImg2show = hierVar.hierEncode(np.array(quartImg), np.array(halfImg))
#Encode whole diff Image
diffF_info, difforgShape, diffrecRGB, diffrecImg2show = hierVar.hierEncode(np.array(halfImg), np.array(imgPIL))


fRecoverHalf, fRecoverHalfImg = hierVar.hireDecode(F_info_quart, halfdiffF_info, halfdifforgShape)
fRecover, fRecoverImg = hierVar.hireDecode(fRecoverHalf, diffF_info, difforgShape)

#fRecoverHalfImg.show()



#tmp.show()
#recImg = quartImg.resize((np.shape(orgRGB)[1], np.shape(orgRGB)[0]))
#recImg.show()

