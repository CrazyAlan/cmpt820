import Tkinter
root = Tkinter.Tk(  )
for r in range(3):
    for c in range(4):
        a = Tkinter.Label(root, text='R%s/C%s'%(r,c),
            borderwidth=1 )
        a.grid(row=r,column=c)
        a.pack()

root.mainloop(  )