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


newDCT = DCT()


print newDCT.T