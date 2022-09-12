import tkinter as tk
from PIL import Image, ImageTk
import cv2
from time import sleep as wait
from functools import partial

window = tk.Tk()

buttonIdentities = []
nameIdentities = []
amounts = []

window.geometry("700x350")

cap= cv2.VideoCapture(0)

class image():
    def __init__(self, amount):
        self.amount = amount

    def capture_image(self, shoot, ename, n):
        global label
        i = 3
        for i in range(3, 0, -1):
            shoot.config(text=str(i))
            window.update()
            wait(1)

        label = tk.Label(window)
        print('doing')
        scale_percent = 25 
        width = int(cap.read()[1].shape[1] * scale_percent / 100)
        height = int(cap.read()[1].shape[0] * scale_percent / 100)
        dim = (width, height)
        
        resized = cv2.resize(cap.read()[1], dim, interpolation = cv2.INTER_AREA)

        cv2image= cv2.cvtColor(resized,cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        
        imgtk = ImageTk.PhotoImage(image = img)          

        label.imgtk = imgtk
        label.configure(image=imgtk)

        label.imgtk = imgtk

        name = ename.get()
        labelName = tk.Label(window, text = str(name))

        if n == 0:
            label.place(x=10, y=100)
            labelName.place(x=70, y=230)
        else:
            l = (2 * (n * 100)) + 10
            label.place(x=l, y=100)
            b = l + 60
            labelName.place(x=b, y=230)

        shoot.destroy()
        ename.destroy()

    def whatClick(self, n):
        print(n)
        ename = (nameIdentities[n])
        bname = (buttonIdentities[n])
        self.capture_image(bname, ename, n)

    def Data(self):
        global var, buttonIdentities, nameIdentities
        p = 10
        i = 0
        for k in range(self.amount):
            shoot = tk.Button(window, text = 'Shoot!!!')
            name = tk.Entry(window) 
            shoot.config(command = partial(self.whatClick, k))
            shoot.place(x=p, y=10)
            name.place(x=p, y=50)
            p += 200
            i+=1
            nameIdentities.append(name)
            buttonIdentities.append(shoot)

def entryGet():
    global Image__
    try:
        Image__ = image(int(entry.get()))
        Image__.Data()
        entry.destroy()
    except ValueError:
        entry.delete('0', tk.END)
        entry.insert('0', 'Not Valid')
        entry.destroy()

entry = tk.Entry(window)
entry.pack()

window.bind('<Return>', lambda event: entryGet())

window.mainloop()