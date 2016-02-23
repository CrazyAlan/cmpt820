import numpy as np
from IntegerTransform improt *
class IntraCoding():
	"""This class is for intra coding and decoding for I frames"""
	def __init__(self):
		#self.deintra_image = []
		self.intra_image = []
		IT = IntegerTransform()

		

	def IntraEncoding(self,Y,Y_r,i,j,N):
		rows = i - 1
		cols = j - 1
		T = Y_r[rows,cols+1:cols+N+1]
		L = Y_r[rows+1:rows+N+1,cols]
		c0 = mode0(Y,T,N)
		c1 = mode0(Y,L,N)
		c2 = mode0(Y,L,T,N)
		BK = Y[rows+1:rows+1+N,cols+1:cols+1+N]
		SOD(0) = sum(sum(abs(c0-BK)))
		SOD(1) = sum(sum(abs(c1-BK)))
		SOD(2) = sum(sum(abs(c2-BK)))
		mode = SOD.index(min(SOD))
		if (mode == 0):
			self.intra_image[i:i+4,j:j+4] = c0
			return BK - c0
		elif (mode == 1):
			self.intra_image[i:i+4,j:j+4] = c1
			return BK - c1
		elif (mode == 2):
			self.intra_image[i:i+4,j:j+4] = c2
			return BK - c2

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
		Y_r = np.zeros_like(Y)
		self.mode = np.zeros((np.shape(Y)[0]//4,np.shape(Y)[1]//4), dtype=np.int)
		for m in range(np.shape(Y)[0]//16):
			for n in range(np.shape(Y)[1]//16):
				for i in range(m*4,m*4+4):
					for j in range(n*4,n*4+4):
						BK = Y[i:i+N,j:j+N]
						if (i == 0 && j == 0):
							mode = 3;
							ICP_en = IT.EnIntegerTransform(BK)
							Y_r = IT.DeIntegerTransform(ICP_en)
						elif (j == 0):
							rows = i - 1
							T = Y_r[rows,cols+1:cols+k+1]
							mode = 0;
							self.intra_image[i*4:i*4+4,j*4:j*4+4] = mode0(Y,T,4)
							ICP = BK - self.intra_image[i*4:i*4+4,j*4:j*4+4]
							ICP_en = IT.EnIntegerTransform(ICP)
							ICP_r = IT.DeIntegerTransform(ICP_en)
							Y_r[i*4:i*4+4,j*4:j*4+4] = self.intra_image[i*4:i*4+4,j*4:j*4+4] + ICP_r
						elif (i == 0):
							cols = j - 1
							L = Y_r[rows+1:rows+k+1,cols]
							mode = 1;
							self.intra_image[i*4:i*4+4,j*4:j*4+4] = mode1(Y,L,4)
							ICP = BK - self.intra_image[i*4:i*4+4,j*4:j*4+4]
							ICP_en = IT.EnIntegerTransform(ICP)
							ICP_r = IT.DeIntegerTransform(ICP_en)
							Y_r[i*4:i*4+4,j*4:j*4+4] = self.intra_image[i*4:i*4+4,j*4:j*4+4] + ICP_r
						else:
							ICP = self.IntraCoding(Y,Y_r,i*4,j*4,4)
							ICP_en = IT.EnIntegerTransform(ICP)
							ICP_r = IT.DeIntegerTransform(ICP_en)
							Y_r[i*4:i*4+4,j*4:j*4+4] = self.intra_image[i*4:i*4+4,j*4:j*4+4] + ICP_r

		return Y_r
		

	'''def IntraDeCodingVec(self,Y):
		self.deintra_image = np.zeros_like(Y)
		for m in range(np.shape(Y)[0]//16):
			for n in range(np.shape(Y)[1]//16):
				for i in range(m*4,m*4+4):
					for j in range(n*4,n*4+4):
						self.IntraDeCoding(Y,self.mode(i,j),i*4,j*4,4)'''
		



	def mode0(self,Y,T,N):
		out = np.zeros_like(Y[0:4,0:4])
		for i in range(N):
			for j in range(N):
				out[i,j] = T[i]
		return out
	def mode1(self,Y,L,N):
		out = np.zeros_like(Y[0:4,0:4])
		for i in range(N):
			for j in range(N):
				out[i,j] = L[i]
		return out
	def mode2(self,Y,L,T,N):
		out = np.zeros_like(Y[0:4,0:4])
		for i in range(N):
			for j in range(N):
				out[i,j] = round(np.mean(np.concatenate(np.concatenate(L[0:N],T[0:N]),np.array([4]))))
		return out
		