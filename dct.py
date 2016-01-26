import numpy as np


class DCT():
	"""docstring for DCT"""
	def __init__(self):
		self.T = []
		self.initT()

	def initT(self):
		tmpT = 0.5*np.ones([8,8])
		tmpT[0,:] *= np.sqrt(2)/2
		for i in xrange(1, 8):
			piArange = np.arange(i,2*i*8,2*i)*np.pi/16
			#print np.cos(piArange)
			tmpT[i, :] *= np.cos(piArange)
		self.T = tmpT
		return self.T

	def dct(self, f):
		F = ((self.T).dot(f)).dot(self.T.transpose())
		return F

	def idct(self, F):
		fRecover = ((self.T.transpose()).dot(F)).dot(self.T)
		return fRecover

	def dctVec(self, fVec):
		F_vec = np.empty_like(fVec)
		for i in xrange(np.shape(fVec)[0]):
			F_vec[i, :, :] = self.dct(fVec[i,:,:])
		return F_vec

	def idctVec(self, FVec):
		f_vec = np.empty_like(FVec)
		for i in xrange(np.shape(FVec)[0]):
			f_vec[i, :, :] = self.idct(FVec[i,:,:])
		return f_vec

	#vectorize the matrix
	@staticmethod
	def vecMat(inMat):
		rows, cols = np.shape(inMat)
		outMat = np.empty([rows*cols/64, 8, 8])
		for i in xrange(0, rows/8):
			for j in xrange(0, cols/8):
				outMat[i*cols/8 + j,:,:] =  inMat[i*8:i*8+8,j*8:j*8+8]
		return outMat

	#devectorize the matrix
	@staticmethod
	def dvecMat(orgMat, inMat):
		rows, cols = np.shape(orgMat)
		outMat = np.empty([rows, cols])
		for i in xrange(0, rows/8):
			for j in xrange(0, cols/8):
				outMat[i*8:i*8+8, j*8:j*8+8] = inMat[i*cols/8 + j, :, :]
		return outMat



'''
tmp = np.random.randint(1,32,[64,128])
tmpOut = DCT.vecMat(tmp)
tmpOutRec = DCT.dvecMat(tmp, tmpOut)
print tmpOutRec - tmp
'''