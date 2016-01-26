import quantization as quant
import numpy as np
import ImageTransform as imt
import dct 

imgQuant = quant.Quantization()
quantMat = np.full([8,8], 1)
imgQuant.initQTMatrix(quantMat)

tmp = np.random.rand(8,8)

tmpQ= imgQuant.quantize(tmp)

print tmpQ