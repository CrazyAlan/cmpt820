import numpy as np
from PIL import Image
import numpy as np
import ImageTransform as imt
import coding 




class Hier():
	"""docstring for Hier"""
	def __init__(self, quantMat):
		self.data = []
		self.IMT = imt.ImageTransform()
		self.quantMat = quantMat

	def hierEncode(self, f_half, f):
		highResShape = np.shape(f)
		E_f_half = imt.ImageTransform.imresize(self.IMT.rgb2img(f_half), highResShape, 1)
		E_f_half_RGB = np.array(E_f_half)

		diffRGB = f - E_f_half_RGB
		F_info, orgShape = coding.encode(np.array(diffRGB), self.quantMat)
		recRGB, recImg2show = coding.decode(F_info, self.quantMat, orgShape)

		return F_info, orgShape, recRGB, recImg2show

	def hireDecode(self, F_info_half, F_info_diff, diffShape):	
		orgHalfShape = (np.array(diffShape[0])/2, np.array(diffShape[1])/2, 3)
		print orgHalfShape
		recRGBHalf, recImg2showHalf = coding.decode(F_info_half, self.quantMat, orgHalfShape)

		#recImg2showHalf.show()
		#diffShape = (np.shape(F_info_diff[0])[0], np.shape(F_info_diff[0])[1], 3)
		print diffShape
		recRGBDiff, recImg2showDiff = coding.decode(F_info_diff, self.quantMat, diffShape)

		#add up
		E_f_half = imt.ImageTransform.imresize(self.IMT.rgb2img(recRGBHalf), diffShape, 1)
		E_f_half_RGB = np.array(E_f_half)

		fRecover = recRGBDiff + E_f_half_RGB
		fRecoverImg = self.IMT.rgb2img(fRecover)

		return fRecover, fRecoverImg


		