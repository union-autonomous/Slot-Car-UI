import tkinter as tk
from PIL import Image, ImageTk
import cv2
from time import sleep as wait
from functools import partial
from tkinter import filedialog as fd
import serial
import threading
from tkinter import ttk

#serial communcation for arduino
serialPort = serial.Serial(port = "COM3", baudrate=115200,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

serialString = ""  

window = tk.Tk()

buttonIdentities = []
nameIdentities = []
frameIdentities = []
oRnameIdentities = []
ChoosenameIdentities = []
chooseImageIdentities = []
lapTimeIdentities = []
bestTimeIdentities = []

window.geometry("1000x650")

bigFrame = tk.Frame(window)

myCanvas = tk.Canvas(master=bigFrame)
myCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

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

        self.Ycords = self.height + 210

        self.lapsRemaining.place(x=0, y=self.Ycords)

        middle = ((250 - self.width) / 2) - 4
        label = tk.Label(self.frame)
        label.imgtk = self.imgtk
        label.configure(image=self.imgtk)
        label.place(x=middle, y=200)
        self.chooseImage.destroy()
    
    def select_file_person(self, percent):
        #Choosing a face from a file

        self.filetypes = (('Images', '*.png'),('All files', '*.*'))
        self.filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=self.filetypes)
    
        self.photo = cv2.imread(self.filename)

        #resizing the photo
        scale_percent = percent 
        self.width = int(self.photo.shape[1] * scale_percent / 100)
        self.height = int(self.photo.shape[0] * scale_percent / 100)
        dim = (self.width, self.height)
        
        if self.width > 160:
            while self.width > 160:
                scale_percent -= 1
                self.width = int(self.photo.shape[1] * scale_percent / 100)
                self.height = int(self.photo.shape[0] * scale_percent / 100)
                dim = (self.width, self.height)
        
        if self.width < 160:
            while self.width < 160:
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
        
        label = tk.Label(self.frame)

        #if Truth equals 0 then take an image from the webcame
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

            if self.width > 160:
                while self.width > 160:
                    scale_percent -= 1
                    self.width = int(cap.read()[1].shape[1] * scale_percent / 100)
                    self.height = int(cap.read()[1].shape[0] * scale_percent / 100)
                    dim = (self.width, self.height)
            
            if self.width < 160:
                while self.width < 160:
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

        #Makes the name for the person that is running the slot car as well as getting the what row it is on
        name = self.ename.get()
        labelName = tk.Label(self.frame, text = str(self.n+1) + ': '+ str(name), font=("Arial", 18))

        self.frame.config(width=250, height=500)

        self.lastLap = tk.Label(self.frame, text = 'Last Lap:')

        self.bestLap = tk.Label(self.frame, text = 'Best Lap:')

        self.lapsRemaining = tk.Label(self.frame, text = 'Laps Remaining:')

        #if button pressed == 0 then place the frame at the start
        if self.n == 0:
            self.frame.place(x=10, y=10)
        #if button pressed is anything but 0 then place using simple formula
        else:
            l = self.n * 300
            self.frame.place(x=l, y=10)

        #place buttons and labels
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
        #Checks what has been pressed
        self.n = n
        self.oRname = (self.oRnameIdentities[self.n])
        self.cname = (self.ChoosenameIdentities[self.n]) 
        self.ename = (self.nameIdentities[self.n])
        self.bname = (self.buttonIdentities[self.n])
        self.frame = (self.frameIdentities[self.n])

        for k in range(self.Players):
            #makes the choose image identities 
            self.chooseImage = tk.Button(self.frame, text='choose image', command = lambda a = 70: self.select_file_car(a))
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
                                lapsRem = tk.Label(self.frame, text=str(LapZero))
                                y = self.Ycords + 30
                                lapsRem.place(x=0, y=y)
                                bestLap = tk.Label(self.frameIdentities[0], text = str(self.string.split(' ')[7]))
                                laps = tk.Label(self.frameIdentities[0], text = str(self.string.split(' ')[4]))
                                bestLap.place(x=0, y=140)
                                laps.place(x=0, y=80)
                            except:
                                pass
                        if self.string.split(' ')[1] == '2':
                            try:
                                bestLap = tk.Label(self.frameIdentities[1], text = str(self.string.split(' ')[7]))
                                laps = tk.Label(self.frameIdentities[1], text = str(self.string.split(' ')[4]))
                                laps.place(x=0, y=80)
                                bestLap.place(x=0, y=140)
                                self.serialtimeOne.append(self.string.split(' ')[4])
                                LapOne-=1
                                lapsRem = tk.Label(self.frame, text=str(LapOne))
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
            frame = tk.Frame(bigFrame, highlightbackground="blue", highlightthickness=2)
            frameIdentities.append(frame)

        myScrollbar = ttk.Scrollbar(master=window, orient=tk.VERTICAL, command=myCanvas.xview)
        myScrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        myCanvas.configure(yscrollcommand=myScrollbar.set)
        myCanvas.bind('<Configure>', lambda e: myCanvas.configure(scrollregion=myCanvas.bbox("all")))
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

Laps = tk.Label(window, text='How Many Laps')
Laps.pack()

laps = tk.Entry(window)
laps.pack()

entryName = tk.Label(window, text='How Many Players')
entryName.pack()

#Makes an entry box to get the amount of players
entry = tk.Entry(window)
entry.pack()

#binds a key to when pressed to entryGet()
window.bind('<Return>', lambda event: entryGet())

window.mainloop()