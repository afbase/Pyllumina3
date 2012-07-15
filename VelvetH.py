from Logger import Logger
import subprocess, os
class VelvetH:
    CurrentDirectory = os.getcwd()
    DEBUG = False
    def __init__(self, LogObject = None, FileName = None, DirectoryName = None, HashLength = 100, FileFormat ='-fasta', ReadType='-shortPaired'):
        """
        (Required) FileName = None
        (Required) DirectoryName = None, the name of the directory to be created 
        HashLength = 100, the kmer length
        FileFormat ='fasta', 
        ReadType='shortPaired'
        """
        self.SetLogObject(LogObject or Logger())
        self.SetFileName(FileName)
        self.SetDirectoryName(DirectoryName)
        self.SetHashLength(HashLength)
        self.SetFileFormat(FileFormat)
        self.SetReadType(ReadType)
        OptionalCommands = self.BuildOptions()
        self.SetOptionalCommands(OptionalCommands)
        
    def SetLogObject(self,LO):
        self.LogObject = LO
    def SetOptionalCommands(self,OC):
        self.OptionalCommands = OC
    def SetFileName(self,FileName):
        self.FileName = FileName
    def SetDirectoryName(self,DirName):
        self.DirectoryName = DirName
    def SetHashLength(self,HashLn):
        self.HashLength = HashLn
    def SetFileFormat(self,FileForm):
        self.FileFormat = FileForm
    def SetReadType(self,ReadType):
        self.ReadType = ReadType
    
    def GetLogObject(self):
        return self.LogObject
    def GetOptionalCommands(self):
        return self.OptionalCommands
    def GetFileName(self):
        return self.FileName
    def GetDirectoryName(self):
        return self.DirectoryName
    def GetHashLength(self):
        return self.HashLength
    def GetFileFormat(self):
        return self.FileFormat
    def GetReadType(self):
        return self.ReadType
    
    def BuildOptions(self, FileName = GetFileName(), DirectoryName = GetDirectoryName(), HashLength = GetHashLength(), FileFormat = GetFileFormat(), ReadType = GetReadType() ):
        """
        This function builds and returns the optional commands for VelvetH
        Input:
        (Required) FileName = None
        (Required) DirectoryName = None, the name of the directory to be created 
        HashLength = 100, the kmer length
        FileFormat ='fasta', 
        ReadType='shortPaired'
        Output:
        velveth output_directory hash_length [[-file_format][-read_type] filename]
        """
        #Text = "velveth %s %s -%s -%s %s" % DirectoryName, str(HashLength), FileFormat, ReadType, FileName
        Text = ['velveth', DirectoryName, str(HashLength), FileFormat, ReadType, FileName]
        return Text 
    def RunStatement(self):
        if self.DEBUG:
            #make a space between each element of the list of metasim commands
            Commands = self.GetOptionalCommands()
            j = ''
            for i in range(len(Commands)):
                Commands[i] = Commands[i] + ' '
                j = j + Commands[i]
            self.SetMetaSimCommand(j)
            os.system(self.GetOptionalCommands()) 
        else:
            if self.GetLogObject() == None:
                Logr = Logger()
                Logr.BuildLogFiles()
            else:
                Logr = self.GetLogObject()
            subprocess.call(self.GetOptionalCommands(),stdin=Logr.InputLog,stderr=Logr.ErrorLog,stdout=Logr.OutputLog)
            