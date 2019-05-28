from SchedulerModule import *


class SRTN(SchedulerModule):
    def __init__(self, AT, BT, ID, ProcessesNum,SwitchTime):
        super().__init__(AT, BT, ID, ProcessesNum,SwitchTime)       # Construct the base class first

        self.Schedule()

    def Schedule(self):

        # An array holds the remaining time for every process.
        Remaining = []
        for i in range(0,self.PN):
            Remaining.append(self.Processes[i].BT)


        # Count equals to processes number and gets reduced by 1 when a process is finished
        count = self.PN

        TimeStamp = 0.0

        # boolean to determine if there's a context switching or not
        DoSwitch = False
        last = -1
        while( count > 0 ):

            min = -1
            # Loop to pick the index of the lowest remaining time
            for i in range(0,self.PN):

                # Ignore the process if it hasn't come yet
                if ( self.Processes[i].AT > TimeStamp ):
                    break
                # Or if it's already finished
                if ( Remaining[i] == 0 ):
                    continue

                elif ( min == -1):
                    min = i

                elif ( Remaining[min] > Remaining[i] ):
                    min = i

            if( min != -1 ):

                if( DoSwitch and last != min ):
                    TimeStamp += self.SwitchTime


                self.GraphAddProcess(TimeStamp,self.Processes[min].ID,0.1)

                TimeStamp += 0.1

                Remaining[min] -= 0.1
                if (Remaining[min] <= 0):
                    Remaining[min] = 0
                    count -= 1
                    self.Processes[min].WT = (TimeStamp+1) - (self.Processes[min].AT + self.Processes[min].BT )

                DoSwitch = True
                last = min

            # No Process is available now ( min = -1 )
            # and will be no context switch next time
            else:
                DoSwitch = False
                TimeStamp += 0.1
