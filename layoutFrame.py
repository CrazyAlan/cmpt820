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
		self.matIndex = (self.matIndex+1)%5
		self.changeMat(quantMat)

		recImage = main.main(quantMat)
		newImage = recImage.resize((384, 256))
		newImage = ImageTk.PhotoImage(newImage)
		self.recphotolabel.image = newImage # keep a reference!
		self.recphotolabel.config(image=newImage)
		print("Change Matrix")

	def changeMat(self, quantMat):
		for r in range(8):
		    for c in range(8):
		        Label(self.matFrame, text='%i'%(quantMat[r,c]),
		            borderwidth=1, padx=2 , pady=2).grid(row=r,column=c)



root = Tk()

randomeMat = np.ones([5,8,8])
for i in xrange(1,5):
	randomeMat[i,:,:] = np.full([8,8], i)*20

lay = layout(root,randomeMat) 

root.mainloop()









