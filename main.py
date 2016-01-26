import coding 
import numpy as np
import scipy as sp
import quantization as quant
import ImageTransform as imt
import dct 


quantMat = np.full([8,8], 1)


orgImage = imt.ImageTransform()
orgRGB = orgImage.readImage("kodim23.png")


imgPIL = orgImage.rgb2img(orgRGB)
halfImg = imgPIL.resize((np.shape(orgRGB)[1]/2, np.shape(orgRGB)[0]/2))
quartImg = imgPIL.resize((np.shape(orgRGB)[1]/4, np.shape(orgRGB)[0]/4))
#tmp.show()
recImg = quartImg.resize((np.shape(orgRGB)[1], np.shape(orgRGB)[0]))
recImg.show()
F_info, orgShape = coding.encode(np.array(quartImg), quantMat)

coding.decode(F_info, quantMat, orgShape)