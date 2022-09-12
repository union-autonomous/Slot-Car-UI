# Import required Libraries
from dis import show_code
import tkinter as tk
from PIL import Image, ImageTk
import cv2
from time import sleep as wait

window = tk.Tk()

amounts = []

window.geometry("700x350")

cap= cv2.VideoCapture(0)

class image():
    def __init__(self, amount):
        self.amount = amount

    def capture_image(self, shoot):
        global label
        i = 3
        for i in range(3, 0, -1):
            shoot.config(text=str(i))
            window.update()
            wait(1)

        label = tk.Label(window)
        scale_percent = 25 # percent of original size
        width = int(cap.read()[1].shape[1] * scale_percent / 100)
        height = int(cap.read()[1].shape[0] * scale_percent / 100)
        dim = (width, height)
        
        # resize image
        resized = cv2.resize(cap.read()[1], dim, interpolation = cv2.INTER_AREA)

        cv2image= cv2.cvtColor(resized,cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)

        imgtk = ImageTk.PhotoImage(image = img)          

        label.imgtk = imgtk
        label.configure(image=imgtk)
        
        if int(var.get()) == 0:
            label.place(x=1, y=100)
        else:
            l = 2 * (var.get() * 100)
            label.place(x=l, y=100)
        shoot.config(text='Shoot!!!')

        label.imgtk = imgtk

    def Data(self):
        global var
        p = 1
        i = 0
        var = tk.IntVar()
        for k in range(self.amount):
            shoot = tk.Radiobutton(window, text = 'Shoot!!!', value = i, variable = var)
            shoot.config(command = lambda shoot = shoot: Image__.capture_image(shoot))
            shoot.place(x=p, y=10)
            p += 200
            i+=1

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