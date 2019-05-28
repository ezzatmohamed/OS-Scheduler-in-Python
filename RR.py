from SchedulerModule import *
from queue import Queue

class RR(SchedulerModule):
    def __init__(self,AT,BT,ID,ProcessesNum,SwitchTime,Quantam):
        super().__init__(AT,BT,ID,ProcessesNum,SwitchTime)         # Construct the base class

        self.Q = Quantam


    def Schedule(self):
            queue = Queue()

            # An array holds the remaining time for every process.
            Remaining = []
            for i in range(0, self.PN):
                Remaining.append(self.Processes[i].BT)

            TimeStamp = 0.0

            count = self.PN  # to count the remaining processes

            DoSwitch = False

            StopIndex = 0
            last = -1
            inserted = False

            while(count > 0):
                inserted = False
                for i in range(0,self.PN):

                    if( Remaining[i] <= 0 ):
                        continue

                    if ( self.Processes[i].AT <= TimeStamp ):
                        queue.put(i)
                        inserted = True
                    else:
                        StopIndex = i
                        break

                if( not inserted ):
                    DoSwitch = False
                    TimeStamp+=0.1

                while not queue.empty():
                    index = queue.get()

                    if ( Remaining[index] > self.Q):


                        if ( DoSwitch and last != index):
                            TimeStamp += self.SwitchTime

                        Remaining[index] -= self.Q

                        self.GraphAddProcess(TimeStamp, self.Processes[index].ID, self.Q)
                        TimeStamp += self.Q

                    else:

                        if( DoSwitch and last != index):
                            TimeStamp+=self.SwitchTime


                        self.GraphAddProcess(TimeStamp, self.Processes[index].ID, Remaining[index])

                        TimeStamp += Remaining[index]

                        Remaining[index] = 0

                        count -= 1
                        self.Processes[index].WT = TimeStamp - (self.Processes[index].AT + self.Processes[index].BT)


                    #if StopIndex >= self.PN :
                     #   StopIndex = 0

                    DoSwitch = True
                    last = index
                    for j in range(StopIndex,self.PN):

                        if (self.Processes[j].AT < TimeStamp and Remaining[j] > 0):
                            queue.put(j)
                            StopIndex+=1
                        else:
                            StopIndex = j
                            break
                    if ( Remaining[index] != 0 ):
                        queue.put(index)
