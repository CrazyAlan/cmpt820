import coding 
import numpy as np


quantMat = np.full([8,8], 100)
F_info, orgShape = coding.encode("kodim23.png", quantMat)

coding.decode(F_info, quantMat, orgShape)