from SchedulerModule import *

class FCFS(SchedulerModule):

    def __init__(self,AT,BT,ID,ProcessesNum,SwitchTime):
        super().__init__(AT,BT,ID,ProcessesNum,SwitchTime)




    def Schedule(self):

        self.Processes[0].WT = 0

        EmptyTime = self.Processes[0].AT

        for i in range(0, self.PN):

            self.Processes[i].WT = EmptyTime - self.Processes[i].AT


            #  self.GraphAddProcess(TimeStamp, self.Processes[min].ID, 1)
            # if the processor is empty when the process arrives then the process won't wait ( wait = 0 ).
            if self.Processes[i].WT < 0:
                self.Processes[i].WT = 0
                # the next time the process will be empty is after the current process finishes

                EmptyTime = self.Processes[i].AT + self.Processes[i].BT
                self.GraphAddProcess(self.Processes[i].AT, self.Processes[i].ID, self.Processes[i].BT)

            else:
                if( i != 0):
                    self.GraphAddProcess(EmptyTime+self.SwitchTime, self.Processes[i].ID, self.Processes[i].BT)
                    EmptyTime = EmptyTime + self.Processes[i].BT+self.SwitchTime
                else:
                    self.GraphAddProcess(EmptyTime, self.Processes[i].ID, self.Processes[i].BT)
                    EmptyTime = EmptyTime + self.Processes[i].BT


    # EndOfFunction
