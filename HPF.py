from SchedulerModule import *


class HPF(SchedulerModule):

    def __init__(self,AT,BT,ID,ProcessesNum,SwitchTime,Priority):
        super().__init__(AT,BT,ID,ProcessesNum,SwitchTime,Priority)


    def Schedule(self):

        TimeStamp = 0.0
        DoSwitch = True

        # An array to determine if every process is finished or not
        done = []
        for i in range(0, self.PN):
            done.append(False)

        count = self.PN

        while(count > 0):

            PriorityIndex = -1

            # a loop to determine the highest priority process
            for i in range(0,self.PN):

                # Ignore the process if it hasn't come yet
                if(self.Processes[i].AT > TimeStamp):
                    break

                # Or if it's already finished
                if  done[i]  :
                    continue

                if PriorityIndex == -1 :
                    PriorityIndex = i
                    continue

                if( self.Processes[i].PT > self.Processes[PriorityIndex].PT):
                    PriorityIndex = i
                elif( self.Processes[i].PT == self.Processes[PriorityIndex].PT ):
                    if( self.Processes[i].ID < self.Processes[PriorityIndex].ID ):
                        PriorityIndex = i


            # No Process is available now ( PriorityIndex = -1 )
            # and will be no context switch next time
            if PriorityIndex ==-1 :
                TimeStamp += 0.1
                DoSwitch = False

            else:

                if(count != self.PN and DoSwitch ):
                    self.Processes[PriorityIndex].WT += self.SwitchTime
                    TimeStamp += self.SwitchTime


                self.GraphAddProcess(TimeStamp,self.Processes[PriorityIndex].ID,self.Processes[PriorityIndex].BT)

                TimeStamp += self.Processes[PriorityIndex].BT

                self.Processes[PriorityIndex].WT = TimeStamp - (self.Processes[PriorityIndex].AT + self.Processes[PriorityIndex].BT)

                done[PriorityIndex] = True
                count -= 1
                DoSwitch = True

