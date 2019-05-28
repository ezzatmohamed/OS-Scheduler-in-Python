# Importing a Library to use Normal and Poisson distribution
import numpy as np

# tkinter for GUI
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd

from SRTN import *
from RR import *
from HPF import *
from FCFS import *
from SchedulerModule import *
class App:
    def __init__(self,master):

        master.title('Processes Generator')
        master.geometry('{}x{}'.format(750, 550))
        x = 0
        y = 24


        self.IFileName = Label(master, text="Choose The Input File :  ")
        self.OFileName = Label(master, text="Output File Name : ")

        self.OEntry = Entry(master)

        self.BrowseFile = Button(text="Select File", command=lambda: self.GetInFile())

        self.IFileName.place(x=x,y=y+5)
        self.BrowseFile.place(x= x+200,y=y,width=200)

        self.Msg1 = Label(master,foreground="red",text ="")
        self.Msg1.place(x=x+420,y =y)

        y +=40
        self.OFileName.place(x=x,y=y)
        self.OEntry.place(x=x+200,y=y,width=200)

        self.SubmitButton = Button(text="Generate Processes" ,command = lambda : self.ProcessGenerator())
        self.SubmitButton.place(x=x+200 , y =y+50,width=200)

        y =y +200
        self.FileProcessLabel = Label(master, text="Processes File : ")
        self.FileProcessLabel.place(x=x,y=y+5)
        self.BrowseFile2 = Button(text="Select Processes File", command=lambda: self.GetProcessFile())
        self.BrowseFile2.place(x= x+200,y=y,width=200)

        self.Msg2 = Label(master, foreground="red", text="")
        self.Msg2.place(x=x + 420, y=y)

       # checkBox1 = Checkbutton(master, onvalue=1, offvalue=0, text="Command  Prompt")
       # checkBox1.place(x=x,y=y+20)
        self.var = IntVar()
        self.var.set(0)

        Radiobutton(master, text="Non-Preemptive Highest Priority First.", variable=self.var, value=1).place(x=x+50 , y=y+30)
        Radiobutton(master, text="First Come First Served.", variable=self.var, value=2).place(x=x+400 , y=y+30)
        Radiobutton(master, text="Round Robin with fixed time quantum", variable=self.var, value=3).place(x=x + 50,y=y + 90)
        Radiobutton(master, text="Preemptive Shortest Remaining Time Next.", variable=self.var, value=4).place(x=x + 400, y=y + 90)


        self.OuantamLabel = Label(master, text="Quantam Time : ")
        self.QuantamTime = Entry(master)

        self.OuantamLabel.place(x=x+50,y=y+111)
        self.QuantamTime.place(x=x + 180,y= y+111, width=50)
        x = x +40
        y = y +111

        self.ContextL = Label(master, text="Context Switching Time : ")
        self.ContextTime = Entry(master)

        self.ContextL.place(x=x + 130, y=y + 50)
        self.ContextTime.place(x=x + 300, y=y + 50, width=50)
        x=x+130
        y=y+50
        self.ScheduleButton = Button(text="Schedule ", command = self.ScheduleAlgo)
        self.ScheduleButton.place(x=x+50,y=y+50,width=150)

    def GetInFile(self):
        self.InFile = fd.askopenfilename()
        self.Msg1['text']= self.InFile

    def GetProcessFile(self):
        self.ProcessFile = fd.askopenfilename()
        self.Msg2['text']= self.ProcessFile

    def ScheduleAlgo(self):

        InputFile = open(self.ProcessFile, "r")
        Lines = InputFile.readlines()

        ProcessNum = int(Lines[0])

        AT = []
        BT = []
        ID = []
        PT = []

        for i in range(1,ProcessNum+1):
            temp = Lines[i].split(' ')
            ID.append(int(temp[0]))
            AT.append(float(temp[1]))
            BT.append(float(temp[2]))
            PT.append(int(temp[3]))
        select = self.var.get()
        if( select == 1):
            Scheduler = HPF(AT,BT,ID,ProcessNum,int(self.ContextTime.get()),PT)
            print("hpf")
        elif( select == 2):
            Scheduler = FCFS(AT,BT,ID,ProcessNum,int(self.ContextTime.get()))
            print("fcfs")
        elif( select == 3):
            print("rr")
            Scheduler = RR(AT,BT,ID,ProcessNum,int(self.ContextTime.get()),int(self.QuantamTime.get()))
        else:
            print("srtn")
            Scheduler = SRTN(AT,BT,ID,ProcessNum,int(self.ContextTime.get()))

        Scheduler.Schedule()

        AvgTT,AvgWTT = Scheduler.TurnaroundTime()
        Processes = Scheduler.Processes

        self.OutFile("ProcessInfo2",Processes,AvgTT,AvgWTT)
        Scheduler.DisplayProcesses()

    def ProcessGenerator(self):
        # Opening the Input File as reading 'r' and Reading all lines into an array - Lines[] -
        InputFile = open(self.InFile, "r")
        Lines = InputFile.readlines()

        # Reading first Line that contains Number of Processes
        ProcessNum = int(Lines[0])

        # Splitting the (  ) of the arrival time and insert them to an array
        temp = Lines[1].split(' ')
        ArrivalT_Factors = [float(temp[0]), float(temp[1])]

        # Splitting the (  ) of the burst time and insert them to an array
        temp = Lines[2].split(' ')
        BurstT_Factors = [float(temp[0]), float(temp[1])]

        # Reading the last line that has the  of priority distribution
        Lam = float(Lines[3])

        # Implementing the Normal Distribution for Arrival Time
        ArriveTime = np.random.normal(ArrivalT_Factors[0], ArrivalT_Factors[1], ProcessNum)
        # Approximate the Numbers to one decimal
        for i in range(0, len(ArriveTime)):
            ArriveTime[i] = round(abs(ArriveTime[i]), 1)

        # Implementing the Normal Distribution for Burst Time
        BurstTime = np.random.normal(BurstT_Factors[0], BurstT_Factors[1], ProcessNum)
        # Approximate the Numbers to one decimal
        for i in range(0, len(BurstTime)):
            BurstTime[i] = round(abs(BurstTime[i]), 1)

        # Implementing the Poisson Distribution for Priority
        Priority = np.random.poisson(Lam, ProcessNum)

        OutputFile = open(self.OEntry.get(), "w")
        OutputFile.write(str(ProcessNum) + "\n")
        for i in range(0, ProcessNum):
            OutputFile.write(
                str(i + 1) + " " + str(ArriveTime[i]) + " " + str(BurstTime[i]) + " " + str(Priority[i]) + "\n")



    def OutFile(self,FileName,Processes,AvgTT,AvgWTT):
        OutputFile = open(FileName,"w")
        OutputFile.write( "ID     Waiting Time    TurnAround Time    Weighted TT    \n")

        for P in Processes :
            OutputFile.write( str(P.ID) + "        " + str( P.WT ) + "           " + str( P.TT ) + "                 "+str(round(P.WTT,2))+"\n")

        OutputFile.write("\n\nAverage TurnAround Time  =     " +str(round(AvgTT,2)) +"\n")
        OutputFile.write("Average Weight Turnaround Time = "+str(round(AvgWTT,2)))
