from Tkinter import *
from PIL import Image, ImageTk
import numpy as np
import main


class layout():
	"""docstring for layout"""
	def __init__(self, master, randomeMat, result, path):
		self.master = master
		self.randomeMat = randomeMat
		self.matIndex = 0
		self.quantMat = self.randomeMat[self.matIndex, :, :]

		self.imgFrame = Frame(bd=3, relief=SUNKEN)
		self.imgFrame.grid(row=0)
		
		self.matFrame = Frame()
		self.matFrame.grid(row=0, column=1,sticky=N)

		self.result = result
		self.path = path
		#self.Frame = Frame()
		#self.matFrame.grid(row=0, column=1)

		self.resultShow()

		self.button2 = Button(self.imgFrame, text="Change Quantization Matrix")
		self.button2.bind("<Button-1>", self.changePhoto) #binding funcs with widgets
		self.button2.grid(row=4, column=0)

		self.changeMat(self.quantMat)

	def resultShow(self):
		image = self.result[0] #original image
		image = image.resize(tuple(np.array(image.size)/2))
		photo = ImageTk.PhotoImage(image)

		Label(self.imgFrame, text="Original Image").grid(row=0, column=0)
		self.photolabel = Label(self.imgFrame, image=photo)
		self.photolabel.image = photo # keep a reference!
		self.photolabel.grid(row = 1, column=0)

		image = self.result[1] #recovered image
		image = image.resize(tuple(np.array(image.size)/2))
		photo = ImageTk.PhotoImage(image)

		Label(self.imgFrame, text="hierachical result").grid(row=2, column=0)
		self.recphotolabel = Label(self.imgFrame, image=photo)
		self.recphotolabel.image = photo # keep a reference!
		self.recphotolabel.grid(row=3,column=0)

		image = self.result[2] #halfdiff image
		image = image.resize(tuple(np.array(image.size)/2))
		photo = ImageTk.PhotoImage(image)

		Label(self.imgFrame, text="halfdiff result").grid(row=0, column=1)
		self.recphotolabel = Label(self.imgFrame, image=photo)
		self.recphotolabel.image = photo # keep a reference!
		self.recphotolabel.grid(row=1,column=1)

		image = self.result[3] #full diff image
		image = image.resize(tuple(np.array(image.size)/2))
		photo = ImageTk.PhotoImage(image)

		Label(self.imgFrame, text="full diff result").grid(row=2, column=1)
		self.recphotolabel = Label(self.imgFrame, image=photo)
		self.recphotolabel.image = photo # keep a reference!
		self.recphotolabel.grid(row=3,column=1)

		image = self.result[4] #half recover image
		image = image.resize(tuple(np.array(image.size)/2))
		photo = ImageTk.PhotoImage(image)

		Label(self.imgFrame, text="half recover result").grid(row=0, column=2)
		self.recphotolabel = Label(self.imgFrame, image=photo)
		self.recphotolabel.image = photo # keep a reference!
		self.recphotolabel.grid(row=1,column=2)

		image = self.result[5] #full recover image
		image = image.resize(tuple(np.array(image.size)/2))
		photo = ImageTk.PhotoImage(image)

		Label(self.imgFrame, text="quarter result").grid(row=2, column=2)
		self.recphotolabel = Label(self.imgFrame, image=photo)
		self.recphotolabel.image = photo # keep a reference!
		self.recphotolabel.grid(row=3,column=2)

	def printMessage(self, event):
		print("it works")


	def changePhoto(self, event):
		quantMat = self.randomeMat[self.matIndex,:,:]
		self.matIndex = (self.matIndex+1)%6
		self.changeMat(quantMat)

		self.result = main.main(quantMat, self.path)
		self.resultShow()
		
		print("Change Matrix")
		print quantMat

	def changeMat(self, quantMat):
		for r in range(8):
		    for c in range(8):
		        Label(self.matFrame, text='%i'%(quantMat[r,c]),
		            borderwidth=1, padx=2 , pady=2).grid(row=r,column=c,sticky=N)

root = Tk()

randomeMat = np.ones([6,8,8])
randomeMat[0,:,:] = np.array([[16,11,10,16,24,40,51,61],[12,12,14,19,26,58,60,55],[14,13,16,24,40,57,69,56],[14,17,22,29,51,87,80,62], [18,22,37,56,68,109,103,77],[24,35,55,64,81,104,113,92],[49,64,78,87,103,121,120,101],[72,92,95,98,112,100,103,99]])
randomeMat[1,:,:] = np.array([[8,5,5,8,12,20,25,30],[6,6,7,9,13,29,30,27],[7,6,8,12,20,28,34,28],[7,8,11,14,25,43,40,31],[9,11,18,28,34,54,51,38],[12,17,27,32,40,52,56,46],[24,32,39,43,51,60,60,50],[36,46,47,49,56,50,51,49]])
randomeMat[2,:,:] = np.array([[64,44,40,64,96,160,204,244],[48,48,56,76,104,232,240,220],[56,52,64,96,160,228,276,224],[56,68,88,116,204,300,300,248],[72,88,148,224,272,300,300,300],[96,140,220,256,300,300,300,300],[196,256,300,300,300,300,300,300],[288,300,300,300,300,300,300,300]])
randomeMat[3,:,:] *= 32
randomeMat[4,:,:] *= 2
randomeMat[5,:,:] *= 128

#[imgPIL fRecoverImg halfdiffrecImg2show diffrecImg2show fRecoverHalfImg recImg2show_quart] = main.main(quantMat)
quantMat = randomeMat[0]
path = "kodim23.png"
result =  main.main(quantMat, path)

lay = layout(root,randomeMat, result, path) 

root.mainloop()









