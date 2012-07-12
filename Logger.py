from subprocess import call
import datetime
import os
import subprocess
class Logger:
    def GetTimeStamp(self):
        now = datetime.datetime.now()
        Time = [ now.year, now.month, now.day, now.hour, now.minute,now.second]
        return Time
    def TimeStamp2String(self,Stamp):
        return ''.join([str(i) for i in Stamp])
    def CreateLog(self,FileName):
        TStr = [str(i) for i in self.INIT_TIME]
        TStr.append(FileName)
        TStr.insert(0, self.Curpath)
        FileName = ''.join(TStr)
        call(['touch',FileName])
        return open(FileName,'a')
    def ErrorMsg(self,txt):
        TimeStamp = self.TimeStamp2String(self.GetTimeStamp())
        ErrorMsg  = 'Error ['+TimeStamp + ']:      ' + txt
        self.ErrorLog.write(ErrorMsg)
    def RunCommand(self,Command):
        """
        Command is a string that is executed, the inputs and outputs are 
        """
        subprocess.call(Command,stdout=self.OutputLog, stdin=self.InputLog, stderr=self.ErrorLog)
    def RunCommandSequence(self,ListOfCommands):
        for X in ListOfCommands:
            self.RunCommand(X)
    def BuildLogFiles(self):
        timestr = self.TimeStamp2String(self.INIT_TIME)
        CurrentDirectory = os.getcwd() + '/'
        Error   = CurrentDirectory + timestr+'Error.Log'
        Output  = CurrentDirectory + timestr+'Output.Log'
        Input   = CurrentDirectory + timestr+'Input.Log'
        self.ErrorLog = file(Error,'w')
        self.OutputLog = file(Output,'w')  
        self.InputLog = file(Input,'w')
    def __init__(self):
        self.Curpath = os.path.abspath(os.curdir)
        self.Curpath += '/'
        self.INIT_TIME = self.GetTimeStamp()            #INIT_TIME must come first
        self.ErrorLog = None
        self.OutputLog = None  
        self.InputLog = None
        
        
