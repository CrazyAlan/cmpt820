from Tkinter import *
from PIL import Image, ImageTk
import numpy as np

class layoutFrame():
	"""docstring for layoutFrame"""
	def __init__(self, master):
		
		self.master = master
		frame = Frame(master)
		frame.pack()
		'''load image'''
		image = Image.open("apple.jpeg")
		photo = ImageTk.PhotoImage(image)


		self.printbutton1 = Button(frame, text="Print Message", command=self.printMessage)
		self.printbutton1.pack(side=LEFT)

		self.quitbutton = Button(frame, text="quit", command=frame.quit)
		self.quitbutton.pack(side=LEFT)


	def printMessage(self):
		print("it works")
		pass

root = Tk()
newFrame = layoutFrame(root)


'''
image = Image.open("apple.jpeg")
photo = ImageTk.PhotoImage(image)
w, h = 512, 512
data = np.zeros((h, w, 3), dtype=np.uint8)
data[256, 256] = [255, 0, 0]
img = Image.fromarray(data, 'RGB')
photo = ImageTk.PhotoImage(img)

print type(image)
print type(photo)
print type(img)
'''

root.mainloop()


