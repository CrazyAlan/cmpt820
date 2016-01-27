import coding 
import numpy as np
import scipy as sp
import quantization as quant
import ImageTransform as imt
import dct 
import hierarchical as hr

def main(quantMat, path):
	#quantMat = np.full([8,8], 1)

	#Read Image
	orgImage = imt.ImageTransform()
	orgRGB = orgImage.readImage(path)

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

	#Decode half 
	recRGB_halfdiff, recImg2show_halfdiff = coding.decode(halfdiffF_info, quantMat, halfdifforgShape)
	fRecoverHalf, fRecoverHalfImg = hierVar.hireDecode(np.array(quartImg), recRGB_halfdiff)
	#fRecoverHalfImg.show()
	#fRecover, fRecoverImg = hierVar.hireDecode(fRecoverHalf, diffF_info, difforgShape)

	#Encode whole diff Image
	#imgPIL.show()
	diffF_info, difforgShape, diffrecRGB, diffrecImg2show = hierVar.hierEncode(np.array(fRecoverHalfImg), np.array(imgPIL))
	#Decode whole image
	recRGB_diff, recImg2show_diff = coding.decode(diffF_info, quantMat, difforgShape)
	fRecover, fRecoverImg = hierVar.hireDecode(np.array(fRecoverHalfImg), recRGB_diff)
	#fRecoverHalfImg.show()
	#fRecoverImg.show()
	return [imgPIL, fRecoverImg, halfdiffrecImg2show ,diffrecImg2show, fRecoverHalfImg ,recImg2show_quart] 

	#fRecoverHalfImg.show()



	#tmp.show()
	#recImg = quartImg.resize((np.shape(orgRGB)[1], np.shape(orgRGB)[0]))
	#recImg.show()

