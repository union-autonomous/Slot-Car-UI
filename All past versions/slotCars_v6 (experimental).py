    def serialReading(self):   
        while(1):
                if(serialPort.in_waiting > 0):
                    self.serialString = serialPort.readline()
                    self.string = self.serialString.decode('Ascii')
                        
                    try:
                        for self.i in range(len(self.frameIdentities)):
                            self.i+=1
                            if self.i == int(self.string.split(' ')[1]):
                                try:
                                    
                                    self.lapRemainingPeople['serialTime'+str(self.i-1)] -=1

                                    if self.labelsCreated == True:
                                        self.laps.configure(text=str(self.string.split(' ')[4]))
                                        self.BestLap.configure(text=str(self.string.split(' ')[7]))
                                        self.lapsRem.configure(text=str(self.lapRemainingPeople['serialTime' + str(self.i)]))
                                        window.update()

                                    elif self.labelsCreated == False:

                                        self.BestLap = tk.CTkLabel(self.frameIdentities[self.i-1], text = str(self.string.split(' ')[7]))
                                        self.laps = tk.CTkLabel(self.frameIdentities[self.i-1], text = str(self.string.split(' ')[4]))
                                        self.lapsRem = tk.CTkLabel(self.frameIdentities[self.i-1], text=str(self.lapRemainingPeople['serialTime' + str(self.i)]))

                                        y = self.yCoordinates[self.i-1] + 30
                                        self.lapsRem.place(x=0, y=y)
                                        self.BestLap.place(x=0, y=140, width=65)
                                        self.laps.place(x=0, y=80, width=65)

                                        self.labelsCreated = True

                                except:
                                    pass
                    except:
                        pass