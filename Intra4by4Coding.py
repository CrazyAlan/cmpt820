import numpy as np

class IntraCoding():
	"""This class is for intra coding and decoding for I frames"""
	def __init__(self):
		
		

	def IntraEncoding(self,Y,i,j,N):
		rows = i - 1
		cols = j - 1
		T = []
		L = []
		for k in range(0,N):
			T = [T,Y(rows,cols+k)]
			L = [L,Y(rows+k,cols)]
		LT = Y(rows,cols)
		c0 = mode0(Y,T,N)
		c1 = mode0(Y,L,N)
		c2 = mode0(Y,L,T,N)
		BK = Y(rows:rows+N,cols:cols+N)
		SOD(0) = sum(sum(abs(c0-BK)))
		SOD(1) = sum(sum(abs(c1-BK)))
		SOD(2) = sum(sum(abs(c2-BK)))
		mode(i,j) = SOD.index(min(SOD))
		if (self.mode == 0):
			self.intra_image(i:i+4,j:j+4) = c0
		elif (self.mode == 1):
			self.intra_image(i:i+4,j:j+4) = c1
		elif (self.mode == 2):
			self.intra_image(i:i+4,j:j+4) = c2
		return mode

	def IntraDecoding(self,Y,mode,i,j,N):
		rows = i - 1
		cols = j - 1
		for k in range(0,2*N):
			T(k) = Y(rows,cols+k)
			L(k) = Y(rows+k,cols)
		LT = Y(rows,cols)
		if (mode == 0):
			self.deintra_image(i:i+4,j:j+4) = mode0(Y,T,N)
		elif (mode == 1):
			self.deintra_image(i:i+4,j:j+4) = mode0(Y,L,N)
		elif (mode == 2):
			self.deintra_image(i:i+4,j:j+4) = mode0(Y,L,T,N)
		elif (mode == 3):
			self.deintra_image(i:i+4,j:j+4) = np.zeros_like(Y(0:4,0:4))
	

	def IntraCodingVec(self,Y):
		self.intra_image = np.zeros_like(Y)
		self.mode = np.zeros((np.shape(Y)[0]//4,np.shape(Y)[1]//4), dtype=np.int)
		for i in range(np.shape(Y)[0]//4):
			for j in range(np.shape(Y)[1]//4):
				if (i == 0 && j == 0):
					self.mode(i,j) = 3;
					self.intra_image(i:i+4,j:j+4) = out = np.zeros_like(Y(0:4,0:4))
				elif (j == 0):
					rows = i - 1
					T = []
					for k in range(0,N):
						T = [T,Y(rows,k)]
					self.mode(i,j) = 0;
					self.intra_image(i:i+4,j:j+4) = mode0(Y,T,4)
				elif (i == 0):
					cols = i - 1
					L = []
					for k in range(0,N):
						L = [L,Y(k,cols)]
					self.mode(i,j) = 1;
					self.intra_image(i:i+4,j:j+4) = mode1(Y,L,4)
				else:
					self.mode(i,j) = self.IntraCoding(Y,i*4,j*4,4)
		

	def IntraDeCodingVec(self,Y):
		self.deintra_image = np.zeros_like(Y)
		for i in range(np.shape(Y)[0]):
			for j in range(np.shape(Y)[0]):
				self.IntraDeCoding(Y,self.mode(i,j),i*4,j*4,4)
		



	def mode0(self,Y,T,N):
		out = np.zeros_like(Y(0:4,0:4))
		for i in range(N):
			for j in range(N):
				out[i][j] = T(i)
		return out
	def mode1(self,Y,L,N):
		out = np.zeros_like(Y(0:4,0:4))
		for i in range(N):
			for j in range(N):
				out[i][j] = L(i)
		return out
	def mode2(self,Y,L,T,N):
		out = np.zeros_like(Y(0:4,0:4))
		for i in range(N):
			for j in range(N):
				out[i][j] = round(np.mean([L(0:N),T(0:N),4]))
		return out
		