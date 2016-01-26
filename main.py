import coding 
import numpy as np
import scipy as sp
import quantization as quant
import ImageTransform as imt
import dct 


quantMat = np.full([8,8], 100)


orgImage = imt.ImageTransform()
orgRGB = orgImage.readImage("kodim23.png")
print np.shape(orgRGB)

F_info, orgShape = coding.encode(orgRGB, quantMat)

coding.decode(F_info, quantMat, orgShape)