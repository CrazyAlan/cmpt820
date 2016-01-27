from Tkinter import *
from PIL import Image, ImageTk
import numpy as np
import main

def printMessage(event):
	print("it works")


def changePhoto( event):
	recImage = main.main(quantMat)
	newImage = recImage.resize((384, 256))
	newImage = ImageTk.PhotoImage(newImage)
	recphotolabel.image = newImage # keep a reference!
	recphotolabel.config(image=newImage)
	print("Change Matrix")

def changeMat(root, quantMat):
	for r in range(8):
	    for c in range(8):
	        Label(root, text='%i'%(quantMat[r,c]),
	            borderwidth=1, padx=2 , pady=2).grid(row=r,column=c)

root = Tk()
imgFrame = Frame(bd=3, relief=SUNKEN)
imgFrame.grid(row=0, sticky=N)


matFrame = Frame()
matFrame.grid(row=0, column=1)

quantMat = np.full([8,8], 2)
changeMat(matFrame, quantMat)


image = Image.open("kodim23.png")
image = image.resize((384, 256))
photo = ImageTk.PhotoImage(image)

Label(imgFrame, text="Original Image").grid(row=0, column=8)
photolabel = Label(imgFrame, image=photo)
photolabel.image = photo # keep a reference!
photolabel.grid(row = 1, column=8)

recphotolabel = Label(imgFrame, image=photo)
recphotolabel.image = photo # keep a reference!
recphotolabel.grid(row=9,column=8)

button2 = Button(imgFrame, text="Change Quantization Matrix")
button2.bind("<Button-1>", changePhoto) #binding funcs with widgets
button2.grid(row=10, column=8)



root.mainloop()









