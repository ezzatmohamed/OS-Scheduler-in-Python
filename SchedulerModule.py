



import matplotlib.pyplot as plt


colors = ['#A52A2A','#D2691E','#F4A460','#D2B48C','#000000','#708090','#8B0000','#FF4500','#BDB76B','#228B22','#808000','#6B8E23','#008080','#191970','#8B008B', '#A9A9A9']



# a Structure For Process Info
class Process:
    def __init__(self,id,at,bt,pt = None):

        self.AT = at            # Arrival Time
        self.ID = id            # Process ID
        self.BT = bt            # Burst Time
        self.PT = pt            # Priority
        self.TT = 0             # TurnAround Time
        self.WTT = 0            # Weight TurnAround Time
        self.WT = 0             # Waiting Time
    #   self.done = False       # for checking if it's finished




#Base Class for every Scheduler Algo
class SchedulerModule:

    def __init__(self, AT, BT, ID,ProcessesNum,SwitchTime,PT=None):

        # Create an array of Processes
        self.Processes = []
        self.SwitchTime = SwitchTime

        # Initializing Processes Array
        for i in range(0,ProcessesNum):
            if( PT == None):
                NewProcess = Process(ID[i] ,AT[i],BT[i])
            else:
                NewProcess = Process(ID[i] ,AT[i],BT[i],PT[i])
            self.Processes.append(NewProcess)


    #    self.TT = []                #Turn Around Time
    #    self.WeightedTT = []        #Weighted Turn Around Time
        self.AvgTT = 0              # TurnAround Time Average
        self.AvgWTT = 0             # Weighted TurnAround Time Average

        self.PN = ProcessesNum      # Number of Processes

        # a 2-dimensional - ( ID - execution time ) - array that holds the final schedule for processes  .
        self.result = []

        # Sorting Processes by Arrival Time

        self.SelectionSort()

    # Calculating TurnAround/Weighted  Time  for every Process and the Average
    def TurnaroundTime(self):

        for i in range(0,self.PN):
            self.Processes[i].TT = self.Processes[i].WT + self.Processes[i].BT
            self.Processes[i].WTT = self.Processes[i].TT / self.Processes[i].BT
            self.AvgTT += self.Processes[i].TT
            self.AvgWTT+= self.Processes[i].WTT

        self.AvgWTT /= self.PN
        self.AvgTT  /= self.PN
        return self.AvgTT,self.AvgWTT


    def GraphAddProcess(self,T,ID,d,DoSwitch=False):

        x = [T, T, T+d,T+d]
        y = [0, ID, ID,0]
        # plotting the line 1 points

        color = ID % ( len(colors) - 1 )
        plt.plot(x, y,color=colors[color])


    def DisplayProcesses(self):
        # naming the x axis
        plt.xlabel('Time')
        # naming the y axis
        plt.ylabel('Process - ID')
        # giving a title to my graph
        # plt.title('')

        # function to show the plot
        plt.show()

    #EndOfMethod


    def Swap(self,x,y):
        temp = x
        x = y
        y = temp
        return x,y

    # An Algorithm to sort Processes by Arrival Time
    def SelectionSort(self):

        min = 0
        length = self.PN  # Get the length of the array
        for i in range(0, length - 1):
            min = i

            # Inner Loop to find the minimum element
            for k in range(i + 1, length):
                if self.Processes[k].AT < self.Processes[min].AT:
                    min = k

            # Moving the minimum element to the index i
            self.Processes[min] , self.Processes[i]  = self.Swap(self.Processes[min],self.Processes[i])


        # End SelectionSort

#End Of Class