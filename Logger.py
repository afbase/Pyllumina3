from subprocess import call
import datetime
import os
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
    def __init__(self):
        self.Curpath = os.path.abspath(os.curdir)
        self.Curpath += '/'
        self.INIT_TIME = self.GetTimeStamp()            #INIT_TIME must come first
        self.ErrorLog = None
        self.OutputLog = None  
        self.InputLog = None
        
        
