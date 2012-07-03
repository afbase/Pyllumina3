class VelvetH:
    def __init__(self, FileName = None, DirectoryName = None, HashLength = 100, FileFormat ='fasta', ReadType='shortPaired'):
        """
        (Required) FileName = None
        (Required) DirectoryName = None, the name of the directory to be created 
        HashLength = 100, the kmer length
        FileFormat ='fasta', 
        ReadType='shortPaired'
        """
        self.SetFileName(FileName)
        self.SetDirectoryName(DirectoryName)
        self.SetHashLength(HashLength)
        self.SetFileFormat(FileFormat)
        self.SetReadType(ReadType)
        OptionalCommands = self.BuildOptions()
        self.SetOptionalCommands(OptionalCommands)
        
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
        Text = "velveth %s %s -%s -%s %s" % DirectoryName, str(HashLength), FileFormat, ReadType, FileName
        return Text 