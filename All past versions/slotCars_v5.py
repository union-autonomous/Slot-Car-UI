from cProfile import label
import tkinter
from PIL import Image, ImageTk
import cv2
from time import sleep as wait
from functools import partial
from tkinter import filedialog as fd
import serial
import threading
import customtkinter as tk

#serial communcation for arduino
serialPort = serial.Serial(port = "COM3", baudrate=115200,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

serialString = ""

window = tk.CTk()

buttonIdentities = []
nameIdentities = []
frameIdentities = []
oRnameIdentities = []
ChoosenameIdentities = []
chooseImageIdentities = []
lapTimeIdentities = []
bestTimeIdentities = []

window.geometry("500x500")

cap = cv2.VideoCapture(0)

class image():
    def __init__(self, Laps, Players, frameIdentities):
        self.Laps = Laps
        self.Players = Players
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
        #Choosing car image from file

        self.filetypes = (('Images', '*.png'),('All files', '*.*'))
        self.filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=self.filetypes)

        self.photo = cv2.imread(self.filename)

        #dynamically resizing the photo to be fitted perfectly in the frame. Also puts the image in the middle
        scale_percent = percent
        self.width = int(self.photo.shape[1] * scale_percent / 100)
        self.height = int(self.photo.shape[0] * scale_percent / 100)
        dim = (self.width, self.height)

        if self.width > 250:
            while self.width > 250:
                scale_percent -= 1
                self.width = int(self.photo.shape[1] * scale_percent / 100)
                self.height = int(self.photo.shape[0] * scale_percent / 100)
                dim = (self.width, self.height)

        if self.width < 250:
            while self.width < 250:
                scale_percent += 1
                self.width = int(self.photo.shape[1] * scale_percent / 100)
                self.height = int(self.photo.shape[0] * scale_percent / 100)
                dim = (self.width, self.height)

        resized = cv2.resize(self.photo, dim, interpolation = cv2.INTER_AREA)

        cv2image = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)

        self.imgtk = ImageTk.PhotoImage(image = img)

        self.Ycords = self.height + 210

        self.lapsRemaining.place(x=0, y=self.Ycords)

        middle = ((270 - self.width) / 2) - 2
        label = tk.CTkLabel(self.frame)  
        label.imgtk = self.imgtk
        label.configure(image=self.imgtk)
        label.place(x=middle, y=200)
        self.chooseImage.destroy()

    def select_file_person(self, percent):
        #Choosing a face from a file

        self.filetypes = (('Images', '*.png'),('All files', '*.*'))
        self.filename = fd .askopenfilename(title='Open a file', initialdir='/', filetypes=self.filetypes)

        self.photo = cv2.imread(self.filename)

        #resizing the photo
        scale_percent = percent 
        self.width = int(self.photo.shape[1] * scale_percent / 100)
        self.height = int(self.photo.shape[0] * scale_percent / 100)
        dim = (self.width, self.height)
        
        if self.width > 180:
            while self.width > 180:
                scale_percent -= 1
                self.width = int(self.photo.shape[1] * scale_percent / 100)
                self.height = int(self.photo.shape[0] * scale_percent / 100)
                dim = (self.width, self.height)
        
        if self.width < 180:
            while self.width < 180:
                scale_percent += 1
                self.width = int(self.photo.shape[1] * scale_percent / 100)
                self.height = int(self.photo.shape[0] * scale_percent / 100)
                dim = (self.width, self.height)

        resized = cv2.resize(self.photo, dim, interpolation = cv2.INTER_AREA)

        cv2image= cv2.cvtColor(resized,cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        
        self.imgtk = ImageTk.PhotoImage(image = img)   

        self.capture_image(1) 

    def capture_image(self, Truth):
        global label

        label = tk.CTkLabel(self.frame)

        #if Truth equals 0 then take an image from the webcam
        if Truth == 0:
            i = 3
            for i in range(3, 0, -1):
                self.bname.configure(text=str(i))
                window.update()
                wait(1)
            
            scale_percent = 25 
            self.width = int(cap.read()[1].shape[1] * scale_percent / 100)
            self.height = int(cap.read()[1].shape[0] * scale_percent / 100)
            dim = (self.width, self.height)

            if self.width > 180:
                while self.width > 180:
                    scale_percent -= 1
                    self.width = int(cap.read()[1].shape[1] * scale_percent / 100)
                    self.height = int(cap.read()[1].shape[0] * scale_percent / 100)
                    dim = (self.width, self.height)
            
            if self.width < 180:
                while self.width < 180:
                    scale_percent += 1
                    self.width = int(cap.read()[1].shape[1] * scale_percent / 100)
                    self.height = int(cap.read()[1].shape[0] * scale_percent / 100)
                    dim = (self.width, self.height)
        
            
            resized = cv2.resize(cap.read()[1], dim, interpolation = cv2.INTER_AREA)

            cv2image= cv2.cvtColor(resized,cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            
            self.imgtk = ImageTk.PhotoImage(image = img) 
        
        #If Truth does not equal 0 then pass the option to grab an image and use the image from a file instead
        else:
            pass
        
        label.imgtk = self.imgtk
        label.configure(image=self.imgtk)

        label.imgtk = self.imgtk

        #Makes the name for the person that is running the slot clar as well as getting the what row it is on
        name = self.ename.get()
        labelName = tk.CTkLabel(self.frame, text = str(self.n+1) + ': ' + str(name), text_font=("Arial", 18))

        self.frame.config(width=270, height=500)

        self.lastLap = tk.CTkLabel(self.frame, text = 'Last Lap:', width = 65)
        self.bestLap = tk.CTkLabel(self.frame, text = 'Best Lap:', width = 65)
        self.lapsRemaining = tk.CTkLabel(self.frame, text = 'Laps Remaining', width = 100)

        b = self.n * 300 + 280

        window.geometry(str(self.winWidth) + 'x550')
        
        if b >= self.winWidth:
            window.geometry(str(b) + 'x550')

        #if button pressed == 0 then place the frame at the start 
        if self.n == 0:
            self.frame.place(x=10, y=10)

        #If button pressed is anything but 0 then place using simple formula
        else:
            l = self.n * 300
            self.frame.place(x=l, y=10)
        
        #place buttons and labels
        self.lastLap.place(x=0, y=60)
        self.bestLap.place(x=0, y=120)
        labelName.place(x=0, y=10)
        label.place(x=120, y=60)

        window.update()
        labelname_width = labelName.winfo_width()
        middle = (250 - labelname_width) / 2

        label_width = label.winfo_width()
        right = (265 - label_width) - 5

        label.place(x=right, y=60)
        labelName.place(x=middle, y=10)

        self.bname.destroy()
        self.ename.destroy()
        self.cname.destroy()
        self.oRname.destroy()

        self.chooseImage.place(x=0, y=200)

    def whatClick(self, n, Truth):
        #Checks what has been pressed
        self.n = n
        self.oRname = (self.oRnameIdentities[self.n])
        self.cname = (self.ChoosenameIdentities[self.n]) 
        self.ename = (self.nameIdentities[self.n])
        self.bname = (self.buttonIdentities[self.n])
        self.frame = (self.frameIdentities[self.n])

        for k in range(self.Players):
            #makes the choose image identities 
            self.chooseImage = tk.CTkButton(self.frame, text='choose image', command = lambda a = 70: self.select_file_car(a))
            self.chooseImageIdentities.append(self.chooseImage)

        self.Choose = (self.ChoosenameIdentities[self.n])

        #checks what truth is
        if Truth == 0:
            self.capture_image(Truth)
        if Truth == 1:
            self.select_file_person(70)

    def Data(self):
        p = 10
        i = 0
        for k in range(self.Players):
            #appends identities for tkinter buttons/widgets
            self.shoot = tk.CTkButton(window, text = 'Shoot', command = partial(self.whatClick, k, 0))
            self.name = tk.CTkEntry(window) 
            self.oR = tk.CTkLabel(window, text='or')
            self.choose = tk.CTkButton(window, text='Image', command = partial(self.whatClick, k, 1))
            
            b = p+60
            z = b+25
            self.shoot.place(x=p, y=10, width=55)
            self.oR.place(x=b, y=10, width=20)
            self.choose.place(x=z, y=10, width=55)
            self.name.place(x=p, y=50)

            p += 300
            i+=1
            self.nameIdentities.append(self.name)
            self.buttonIdentities.append(self.shoot)
            self.ChoosenameIdentities.append(self.choose)
            self.oRnameIdentities.append(self.oR)   
        
        if self.Players == 1:
            self.winWidth = 160
            window.geometry(str(self.winWidth) + 'x250')
        
        else:
            self.winWidth = (self.Players * 300) - 140
            window.geometry(str(self.winWidth) + 'x250')

    def serialReading(self):    
        #not important right now (for reading serial arduino)
        self.serialtimeZero = []
        self.serialtimeOne = []
        i = 0
        LapZero = self.Laps
        LapOne = self.Laps
        while(1):
                if(serialPort.in_waiting > 0):
                    self.list = []
                    self.serialString = serialPort.readline()
                    self.string = self.serialString.decode('Ascii')
                        
                    try:  
                        if self.string.split(' ')[1] == '1':
                            try:
                                self.serialtimeZero.append(self.string.split(' ')[4])
                                LapZero-=1
                                print(LapZero)
                                lapsRem = tk.CTkLabel(self.frame, text=str(LapZero))
                                y = self.Ycords + 30
                                lapsRem.place(x=0, y=y)
                                bestLap = tk.CTkLabel(self.frameIdentities[0], text = str(self.string.split(' ')[7]))
                                laps = tk.CTkLabel(self.frameIdentities[0], text = str(self.string.split(' ')[4]))
                                bestLap.place(x=0, y=140)
                                laps.place(x=0, y=80)
                            except:
                                pass
                        if self.string.split(' ')[1] == '2':
                            try:
                                bestLap = tk.CTkLabel(self.frameIdentities[1], text = str(self.string.split(' ')[7]))
                                laps = tk.CTkLabel(self.frameIdentities[1], text = str(self.string.split(' ')[4]))
                                laps.place(x=0, y=80)
                                bestLap.place(x=0, y=140)
                                self.serialtimeOne.append(self.string.split(' ')[4])
                                LapOne-=1
                                lapsRem = tk.CTkLabel(self.frame, text=str(LapOne))
                                y = self.Ycords + 30
                                lapsRem.place(x=0, y=y)
                            except:
                                pass
                    except:
                        pass

def entryGet():
    global Image__

    def frames(Players):
        #makes frame identities
        global frameIdentities
        for data in range(Players):
            frame = tk.CTkFrame(window, highlightbackground="blue", highlightthickness=2)
            frameIdentities.append(frame)

    try:
        #Tries to do class 
        Players = int(entry.get())
        frames(Players)
        Image__ = image(Laps, Players, frameIdentities)
        Image__.Data()
        entry.destroy()
        entryName.destroy()
        laps.destroy()
        Laps.destroy()
    except ValueError:
        #if entry is not a number then don't for class
        entry.delete('0', tk.END)
        entry.insert('0', 'Not Valid')  

Laps = tk.CTkLabel(window, text='How Many Laps')
Laps.pack()

laps = tk.CTkEntry(window)
laps.pack()

entryName = tk.CTkLabel(window, text='How Many Players')
entryName.pack()

#Makes an entry box to get the amount of players
entry = tk.CTkEntry(window)
entry.pack()

#binds a key to when pressed to entryGet()
window.bind('<Return>', lambda event: entryGet())

window.mainloop()               