import numpy as np
from IntegerTransform import *
class IntraCoding():
	"""This class is for intra coding and decoding for I frames"""
	def __init__(self,QP):
		#self.deintra_image = []
		self.intra_image = []
		self.IT = IntegerTransform()
		self.IT.QuantizationMatrix(QP)
		

	def IntraEncoding(self,Y,Y_r,i,j,N):
		rows = i - 1
		cols = j - 1
		T = Y_r[rows,cols+1:cols+N+1]
		L = Y_r[rows+1:rows+N+1,cols]
		c0 = self.mode0(Y,T,N)
		c1 = self.mode1(Y,L,N)
		c2 = self.mode2(Y,L,T,N)
		BK = Y[rows+1:rows+1+N,cols+1:cols+1+N]
		SOD = [0,0,0]
		SOD[0] = sum(sum(abs(c0-BK)))
		SOD[1] = sum(sum(abs(c1-BK)))
		SOD[2] = sum(sum(abs(c2-BK)))
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
		for m in range(np.shape(Y)[0]//16):
			for n in range(np.shape(Y)[1]//16):
				for i in range(m*4,m*4+4):
					for j in range(n*4,n*4+4):
						BK = Y[i*4:i*4+4,j*4:j*4+4]
						if (i == 0 and j == 0):
							mode = 3
							ICP_en = self.IT.EnIntegerTransform(BK)
							Y_r[i*4:i*4+4,j*4:j*4+4] = self.IT.DeIntegerTransform(ICP_en)
						elif (j == 0):
							rows = i - 1
							T = Y_r[rows,0:4]
							mode = 0
							self.intra_image[i*4:i*4+4,j*4:j*4+4] = self.mode0(Y,T,4)
							ICP = BK - self.intra_image[i*4:i*4+4,j*4:j*4+4]
							ICP_en = self.IT.EnIntegerTransform(ICP)
							ICP_r = self.IT.DeIntegerTransform(ICP_en)
							Y_r[i*4:i*4+4,j*4:j*4+4] = self.intra_image[i*4:i*4+4,j*4:j*4+4] + ICP_r
						elif (i == 0):
							cols = j - 1
							L = Y_r[0:4,cols]
							mode = 1
							self.intra_image[i*4:i*4+4,j*4:j*4+4] = self.mode1(Y,L,4)
							ICP = BK - self.intra_image[i*4:i*4+4,j*4:j*4+4]
							ICP_en = self.IT.EnIntegerTransform(ICP)
							ICP_r = self.IT.DeIntegerTransform(ICP_en)
	
							Y_r[i*4:i*4+4,j*4:j*4+4] = self.intra_image[i*4:i*4+4,j*4:j*4+4] + ICP_r
						else:
							ICP = self.IntraEncoding(Y,Y_r,i*4,j*4,4)
							ICP_en = self.IT.EnIntegerTransform(ICP)
							ICP_r = self.IT.DeIntegerTransform(ICP_en)
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
				out[i,j] = round(np.mean(np.concatenate([L,T]))+4/9.0)
		return out

if __name__ == '__main__':
	Y = np.load("Y.npy")
	IC = IntraCoding(30)
	Y_r = IC.IntraCodingVec(Y)
	print np.shape(Y_r)
	#np.save("Y_r.npy",Y_r)
		