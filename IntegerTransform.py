import numpy as np
#from ImageTransform import *

class IntegerTransform():
	"""docstring for IntegerTransfrom"""
	def __init__(self):
		self.m = []
		self.v = []

		self.H = np.array([[1,1,1,1],[2,1,-1,-2],[1,-1,-1,1],[1,-2,2,-1]])
		self.Hinv = np.array([[1,1,1,1/2.0],[1,1/2.0,-1,-1],[1,-1/2.0,-1,1],[1,-1,1,-1/2.0]])
		self.Q_ori = np.array([[13107,5243,8066,10,16,13],[11916,4660,7490,11,18,14],[10082,4194,6554,13,20,16],[9362,3647,5825,14,23,18],[8192,3355,5243,16,25,20],[7282,2893,4559,18,29,23]])
		
	def QuantizationMatrix(self,QP):
		Q = np.concatenate((self.Q_ori[QP%6,0:3]/(2**(QP//6)), self.Q_ori[QP%6,3:6]*(2**(QP//6))) )
		self.m = np.array([[Q[0],Q[2],Q[0],Q[2]],[Q[2],Q[1],Q[2],Q[1]],[Q[0],Q[2],Q[0],Q[2]],[Q[2],Q[1],Q[2],Q[1]]])
		self.v = np.array([[Q[3],Q[5],Q[3],Q[5]],[Q[5],Q[4],Q[5],Q[4]],[Q[3],Q[5],Q[3],Q[5]],[Q[5],Q[4],Q[5],Q[4]]])
	
	def EnIntegerTransform(self,f):
		tmp1 = (self.H).dot(f) 
		tmp2 = tmp1.dot(np.transpose(self.H))
		F_hat = np.round((tmp2)*self.m/(2**15))
		return F_hat
	
	def DeIntegerTransform(self,F_hat):
		f_hat = np.round(self.Hinv.dot((F_hat*self.v).dot(np.transpose(self.Hinv)))/(2**6))
		return f_hat

	def EnIntegerTransformVec(self, fvec):
		F_hat_vec = np.zeros_like(fvec)
		for i in range(np.shape(fvec)[0]):
			F_hat_vec[i,:,:] = self.EnIntegerTransform(fvec[i,:,:])
		return F_hat_vec

	def DeIntegerTransformVec(self, F_hat_vec):
		F_hatRevoverd_vec = np.zeros_like(F_hat_vec)
		for i in range(np.shape(F_hat_vec)[0]):
			F_hatRevoverd_vec[i,:,:] = self.DeIntegerTransform(F_hat_vec[i,:,:])
		return F_hatRevoverd_vec


if __name__ == '__main__':
	IT = IntegerTransform()
	IT.QuantizationMatrix(6)

	IMT = ImageTransform()
	test = np.array([[72,82,85,79], [74,75,86,82],[84,73,78,80],[77,81,76,84]])	

	trans = IT.EnIntegerTransform(test)
	
	dtrans = IT.DeIntegerTransform(trans)

	print trans
	print dtrans
	
	
