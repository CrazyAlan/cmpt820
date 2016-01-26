import numpy as np


class Quantization():
	"""docstring for Quantization"""
	def __init__(self):
		self.QuantMatrix = []

	def initQTMatrix(self, QTmat):
		self.QuantMatrix = QTmat

	def quantize(self, F):
		F_hat = np.round(F/self.QuantMatrix)
		return F_hat

	def dquantize(self, F_hat):
		F_hatRevoverd = F_hat*self.QuantMatrix
		return F_hatRevoverd

	def quanitzeVec(self, Fvec):
		F_hat_vec = np.empty_like(Fvec)
		for i in xrange(np.shape(Fvec)[0]):
			F_hat_vec[i,:,:] = self.quantize(Fvec[i,:,:])
		return F_hat_vec

	def dquanitzeVec(self, F_hat_vec):
		F_hatRevoverd_vec = np.empty_like(F_hat_vec)
		for i in xrange(np.shape(F_hat_vec)[0]):
			F_hatRevoverd_vec[i,:,:] = self.dquantize(F_hat_vec[i,:,:])
		return F_hatRevoverd_vec



'''
qtmat = np.random.randint(1,4,size=(8,8))
tmpf = np.random.randint(50,234,size=(8,8))

qt = Quantization()
qt.initQTMatrix(qtmat)

tmpF = qt.quantize(tmpf)

tmpfR = qt.dquantize(tmpF)

print tmpfR - tmpf
print qtmat
'''

		