from Tkinter import *
from PIL import Image, ImageTk
import numpy as np
import main


class layout():
	"""docstring for layout"""
	def __init__(self, master, randomeMat):
		self.master = master
		self.randomeMat = randomeMat
		self.matIndex = 1
		self.quantMat = self.randomeMat[self.matIndex, :, :]

		self.imgFrame = Frame(bd=3, relief=SUNKEN)
		self.imgFrame.grid(row=0)
		
		self.matFrame = Frame()
		self.matFrame.grid(row=0, column=1)

		image = Image.open("kodim23.png")
		image = image.resize((384, 256))
		photo = ImageTk.PhotoImage(image)

		Label(self.imgFrame, text="Original Image").grid(row=0, column=8)
		self.photolabel = Label(self.imgFrame, image=photo)
		self.photolabel.image = photo # keep a reference!
		self.photolabel.grid(row = 1, column=8)

		self.recphotolabel = Label(self.imgFrame, image=photo)
		self.recphotolabel.image = photo # keep a reference!
		self.recphotolabel.grid(row=9,column=8)

		self.button2 = Button(self.matFrame, text="Change Quantization Matrix")
		self.button2.bind("<Button-1>", self.changePhoto) #binding funcs with widgets
		self.button2.grid(row=10, column=8)

		self.changeMat(self.quantMat)

	def printMessage(self, event):
		print("it works")


	def changePhoto(self, event):
		quantMat = self.randomeMat[self.matIndex,:,:]
		self.matIndex = (self.matIndex+1)%6
		self.changeMat(quantMat)

		recImage = main.main(quantMat)
		newImage = recImage.resize((384, 256))
		newImage = ImageTk.PhotoImage(newImage)
		self.recphotolabel.image = newImage # keep a reference!
		self.recphotolabel.config(image=newImage)
		print("Change Matrix")
		print quantMat

	def changeMat(self, quantMat):
		for r in range(8):
		    for c in range(8):
		        Label(self.matFrame, text='%i'%(quantMat[r,c]),
		            borderwidth=1, padx=2 , pady=2).grid(row=r,column=c)

root = Tk()

randomeMat = np.ones([6,8,8])
randomeMat[0,:,:] = np.array([[16,11,10,16,24,40,51,61],[12,12,14,19,26,58,60,55],[14,13,16,24,40,57,69,56],[14,17,22,29,51,87,80,62], [18,22,37,56,68,109,103,77],[24,35,55,64,81,104,113,92],[49,64,78,87,103,121,120,101],[72,92,95,98,112,100,103,99]])
randomeMat[1,:,:] = np.array([[8,5,5,8,12,20,25,30],[6,6,7,9,13,29,30,27],[7,6,8,12,20,28,34,28],[7,8,11,14,25,43,40,31],[9,11,18,28,34,54,51,38],[12,17,27,32,40,52,56,46],[24,32,39,43,51,60,60,50],[36,46,47,49,56,50,51,49]])
randomeMat[2,:,:] = np.array([[64,44,40,64,96,160,204,244],[48,48,56,76,104,232,240,220],[56,52,64,96,160,228,276,224],[56,68,88,116,204,300,300,248],[72,88,148,224,272,300,300,300],[96,140,220,256,300,300,300,300],[196,256,300,300,300,300,300,300],[288,300,300,300,300,300,300,300]])
randomeMat[3,:,:] *= 32
randomeMat[4,:,:] *= 2
randomeMat[5,:,:] *= 128


lay = layout(root,randomeMat) 

root.mainloop()









