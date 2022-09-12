import tkinter as tk
from PIL import Image, ImageTk
import cv2
from time import sleep as wait
from functools import partial
from tkinter import filedialog as fd
import serial
import threading

serialPort = serial.Serial(port = "COM3", baudrate=9600,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

serialString = ""  

window = tk.Tk()

buttonIdentities = []
nameIdentities = []
frameIdentities = []
amounts = []
oRnameIdentities = []
ChoosenameIdentities = []
chooseImageIdentities = []
lapTimeIdentities = []
bestTimeIdentities = []

window.geometry("1000x650")

cap = cv2.VideoCapture(0)

class image():
    def __init__(self, amount, frameIdentities):
        self.amount = amount
        self.nameIdentities = nameIdentities
        self.buttonIdentities = buttonIdentities
        self.frameIdentities = frameIdentities
        self.oRnameIdentities = oRnameIdentities
        self.ChoosenameIdentities = ChoosenameIdentities
        self.chooseImageIdentities = chooseImageIdentities
        self.lapTimeIdentities = lapTimeIdentities
        self.bestTimeIdentities = bestTimeIdentities
        threading.Thread(target=self.serialReading).start()
    
    def select_file_car(self, percent):
        
        self.filetypes = (('Images', '*.png'),('All files', '*.*'))
        self.filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=self.filetypes)
    
        self.photo = cv2.imread(self.filename)

        scale_percent = percent 
        self.width = int(self.photo.shape[1] * scale_percent / 100)
        self.height = int(self.photo.shape[0] * scale_percent / 100)
        dim = (self.width, self.height)
        
        if self.width > 230:
            while self.width > 230:
                scale_percent -= 1
                self.width = int(self.photo.shape[1] * scale_percent / 100)
                self.height = int(self.photo.shape[0] * scale_percent / 100)
                dim = (self.width, self.height)
        
        if self.width < 230:
            while self.width < 230:
                scale_percent += 1
                self.width = int(self.photo.shape[1] * scale_percent / 100)
                self.height = int(self.photo.shape[0] * scale_percent / 100)
                dim = (self.width, self.height)
        
        resized = cv2.resize(self.photo, dim, interpolation = cv2.INTER_AREA)

        cv2image= cv2.cvtColor(resized,cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        
        self.imgtk = ImageTk.PhotoImage(image = img)   

        a = self.height + 210

        self.lapsRemaining.place(x=0, y=a)

        middle = ((250 - self.width) / 2) - 4
        label = tk.Label(self.frame)
        label.imgtk = self.imgtk
        label.configure(image=self.imgtk)
        label.place(x=middle, y=200)
        self.chooseImage.destroy()
    
    def select_file_person(self, percent):
        
        self.filetypes = (('Images', '*.png'),('All files', '*.*'))
        self.filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=self.filetypes)
    
        self.photo = cv2.imread(self.filename)

        scale_percent = percent 
        width = int(self.photo.shape[1] * scale_percent / 100)
        height = int(self.photo.shape[0] * scale_percent / 100)
        dim = (width, height)
        
        resized = cv2.resize(self.photo, dim, interpolation = cv2.INTER_AREA)

        cv2image= cv2.cvtColor(resized,cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        
        self.imgtk = ImageTk.PhotoImage(image = img)   

        self.capture_image(1)

    def capture_image(self, Truth):
        global label
        
        label = tk.Label(self.frame)

        if Truth == 0:
            i = 3
            for i in range(3, 0, -1):
                self.bname.config(text=str(i))
                window.update()
                wait(1)

            scale_percent = 25 
            self.width = int(cap.read()[1].shape[1] * scale_percent / 100)
            self.height = int(cap.read()[1].shape[0] * scale_percent / 100)
            dim = (self.width, self.height)
            
            resized = cv2.resize(cap.read()[1], dim, interpolation = cv2.INTER_AREA)

            cv2image= cv2.cvtColor(resized,cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            
            self.imgtk = ImageTk.PhotoImage(image = img) 

        else:
            pass         

        label.imgtk = self.imgtk
        label.configure(image=self.imgtk)

        label.imgtk = self.imgtk

        name = self.ename.get()
        labelName = tk.Label(self.frame, text = str(self.n+1) + ': '+ str(name), font=("Arial", 18))

        self.frame.config(width=250, height=500)

        self.lastLap = tk.Label(self.frame, text = 'Last Lap:')

        self.bestLap = tk.Label(self.frame, text = 'Best Lap:')

        self.lapsRemaining = tk.Label(self.frame, text = 'Laps Remaining:')

        if self.n == 0:
            self.frame.place(x=10, y=10)
        else:
            l = self.n * 300
            self.frame.place(x=l, y=10)

        self.lastLap.place(x=0, y=60)
        self.bestLap.place(x=0, y=120)
        labelName.place(x=0, y=10)
        label.place(x=130, y=60)
        
        window.update()
        labelname_width = labelName.winfo_width()
        middle = (250 - labelname_width) / 2

        label_width = label.winfo_width()
        right = (250 - label_width) - 5
        
        label.place(x=right, y=60)
        labelName.place(x=middle, y=10)

        self.bname.destroy()
        self.ename.destroy()
        self.cname.destroy()
        self.oRname.destroy()

        self.chooseImage.place(x=0, y=200)

    def whatClick(self, n, Truth):
        self.n = n
        self.oRname = (self.oRnameIdentities[self.n])
        self.cname = (self.ChoosenameIdentities[self.n]) 
        self.ename = (self.nameIdentities[self.n])
        self.bname = (self.buttonIdentities[self.n])
        self.frame = (self.frameIdentities[self.n])

        for k in range(self.amount):
            self.Lastlaptime = tk.Label(self.frame, text = '0.00')
            self.bestlaptime = tk.Label(self.frame, text = '0.00')
            self.chooseImage = tk.Button(self.frame, text='choose image', command = lambda a = 70: self.select_file_car(a))

            self.chooseImageIdentities.append(self.chooseImage)
            self.bestTimeIdentities.append(self.bestlaptime)
            self.lapTimeIdentities.append(self.Lastlaptime)

        self.lapTime = (self.lapTimeIdentities[self.n])
        self.bestTime = (self.bestTimeIdentities[self.n])
        self.Choose = (self.ChoosenameIdentities[self.n])

        if Truth == 0:
            self.capture_image(Truth)
        if Truth == 1:
            self.select_file_person(70)

    def Data(self):
        p = 10
        i = 0
        for k in range(self.amount):
            self.shoot = tk.Button(window, text = 'Shoot!!!')
            self.name = tk.Entry(window) 
            self.oR = tk.Label(window, text='or')
            self.choose = tk.Button(window, text='Choose Image', command = partial(self.whatClick, k, 1))
            self.shoot.config(command = partial(self.whatClick, k, 0))
            
            b = p+60
            z = b+25
            self.shoot.place(x=p, y=10)
            self.oR.place(x=b, y=10)
            self.choose.place(x=z, y=10)
            self.name.place(x=p, y=50)

            p += 300
            i+=1
            self.nameIdentities.append(self.name)
            self.buttonIdentities.append(self.shoot)
            self.ChoosenameIdentities.append(self.choose)
            self.oRnameIdentities.append(self.oR)

    def serialReading(self):
        self.serialtime = []
        while(1):

            if(serialPort.in_waiting > 0):
                self.list = []
                self.serialString = serialPort.readline()
                self.string = self.serialString.decode('Ascii')  
                try:
                    self.lapTime.config(text = str(self.string.split(' ')[4]))
                    self.lapTime.place(x=0, y=80)
                    self.serialtime = []
                except:
                    pass

def entryGet():
    global Image__

    def frames(Amount):
        global frameIdentities
        for data in range(Amount):
            frame = tk.Frame(window, highlightbackground="blue", highlightthickness=2)
            frameIdentities.append(frame)
    try:
        Amount = int(entry.get())
        frames(Amount)
        Image__ = image(Amount, frameIdentities)
        Image__.Data()
        entry.destroy()
    except ValueError:
        frames(Amount)
        entry.delete('0', tk.END)
        entry.insert('0', 'Not Valid')
        entry.destroy()

entry = tk.Entry(window)
entry.pack()

window.bind('<Return>', lambda event: entryGet())

window.mainloop()