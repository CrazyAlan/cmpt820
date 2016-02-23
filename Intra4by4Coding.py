import numpy as np
from IntegerTransform improt *
class IntraCoding():
	"""This class is for intra coding and decoding for I frames"""
	def __init__(self):
		self.deintra_image = []
		self.intra_image = []
		

	def IntraEncoding(self,Y,Y_r,i,j,N):
		rows = i - 1
		cols = j - 1
		T = Y[rows,cols+1:cols+k+1]
		L = Y[rows+1:rows+k+1,cols]
		c0 = mode0(Y,T,N)
		c1 = mode0(Y,L,N)
		c2 = mode0(Y,L,T,N)
		BK = Y(rows:rows+N,cols:cols+N)
		SOD(0) = sum(sum(abs(c0-BK)))
		SOD(1) = sum(sum(abs(c1-BK)))
		SOD(2) = sum(sum(abs(c2-BK)))
		mode(i,j) = SOD.index(min(SOD))
		if (self.mode == 0):
			self.intra_image[i:i+4,j:j+4] = c0
		elif (self.mode == 1):
			self.intra_image[i:i+4,j:j+4] = c1
		elif (self.mode == 2):
			self.intra_image[i:i+4,j:j+4] = c2
		return mode

	'''def IntraDecoding(self,Y,mode,i,j,N):
		rows = i - 1
		cols = j - 1
		for k in range(0,2*N):
			T(k) = Y(rows,cols+k)
			L(k) = Y(rows+k,cols)
		if (mode == 0):
			self.deintra_image(i:i+4,j:j+4) = mode0(Y,T,N)
		elif (mode == 1):
			self.deintra_image(i:i+4,j:j+4) = mode1(Y,L,N)
		elif (mode == 2):
			self.deintra_image(i:i+4,j:j+4) = mode2(Y,L,T,N)
		elif (mode == 3):
			self.deintra_image(i:i+4,j:j+4) = np.zeros_like(Y(0:4,0:4))'''
	

	def IntraCodingVec(self,Y):
		self.intra_image = np.zeros_like(Y)
		self.mode = np.zeros((np.shape(Y)[0]//4,np.shape(Y)[1]//4), dtype=np.int)
		for m in range(np.shape(Y)[0]//16):
			for n in range(np.shape(Y)[1]//16):
				for i in range(m*4,m*4+4):
					for j in range(n*4,n*4+4):
						if (i == 0 && j == 0):
							self.mode(i,j) = 3;
							self.intra_image[i*4:i*4+4,j*4:j*4+4] = np.zeros_like(Y(0:4,0:4))
						elif (j == 0):
							rows = i - 1
							T = Y[rows,cols+1:cols+k+1]
							self.mode(i,j) = 0;
							self.intra_image[i*4:i*4+4,j*4:j*4+4] = mode0(Y,T,4)
						elif (i == 0):
							cols = j - 1
							L = Y[rows+1:rows+k+1,cols]
							self.mode(i,j) = 1;
							self.intra_image[i*4:i*4+4,j*4:j*4+4] = mode1(Y,L,4)
						else:
							self.mode(i,j) = self.IntraCoding(Y,Y_r,i*4,j*4,4)
		

	'''def IntraDeCodingVec(self,Y):
		self.deintra_image = np.zeros_like(Y)
		for m in range(np.shape(Y)[0]//16):
			for n in range(np.shape(Y)[1]//16):
				for i in range(m*4,m*4+4):
					for j in range(n*4,n*4+4):
						self.IntraDeCoding(Y,self.mode(i,j),i*4,j*4,4)'''
		



	def mode0(self,Y,T,N):
		out = np.zeros_like(Y(0:4,0:4))
		for i in range(N):
			for j in range(N):
				out[i,j] = T(i)
		return out
	def mode1(self,Y,L,N):
		out = np.zeros_like(Y(0:4,0:4))
		for i in range(N):
			for j in range(N):
				out[i,j] = L(i)
		return out
	def mode2(self,Y,L,T,N):
		out = np.zeros_like(Y(0:4,0:4))
		for i in range(N):
			for j in range(N):
				out[i,j] = round(np.mean([L(0:N),T(0:N),4]))
		return out
		