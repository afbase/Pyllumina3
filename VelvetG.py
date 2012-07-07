class VelvetG:
    def __init__(self, OutputFolder=None, CoverageCutoff=None, MinContigLength=None, ExpCov=None, MaxCov=None, InsertLength=None):
        """
        (required) OutputFolder = Output Directory of DeBruijn Graph Results
        CoverageCutoff = Minimum amount of times a base pair is sequenced
        MinContigLength = The smallest continuous sequenced length output desired
        ExpCov = The expected coverage of times a base pair is sequenced 
        MaxCov = the largest amount of times a base pair is sequenced
        (requires pairs ends option in velveth) InsertLength = To activate the use of read pairs, you must specify two parameters: the
                                                                expected (i.e. average) insert length (or at least a rough estimate), and the
                                                                expected short-read k-mer coverage (see 5.1 for more information)
        """
        self.SetCoverageCutoff(CoverageCutoff)
        self.SetMinContigLength(MinContigLength)
        self.SetExpCov(ExpCov)
        self.SetMaxCov(MaxCov)
        self.SetInsertLength(InsertLength)
        self.SetOutputFolder(OutputFolder)
        Command = self.BuildCommand()
        self.SetCommand(Command)
    
    def SetOutputFolder(self,OF):
        self.OutputFolder = OF
    def SetCoverageCutoff(self,CC):
        self.CoverageCutoff = CC
    def SetMinContigLength(self,MCL):
        self.MinContigLength = MCL
    def SetExpCov(self,EC):
        self.ExpCov = EC
    def SetMaxCov(self,MC):
        self.MaxCov = MC
    def SetInsertLength(self,IL):
        self.InsertLength = IL
    def SetCommand(self,C):
        self.Command = C
    
    def GetCommand(self,C):
        return self.Command
    def GetOutputFolder(self):
        return self.OutputFolder
    def GetCoverageCutoff(self):
        return self.CoverageCutoff
    def GetMinContigLength(self):
        return self.MinContigLength
    def GetExpCov(self):
        return self.ExpCov
    def GetMaxCov(self):
        return self.MaxCov
    def GetInsertLength(self):
        return self.InsertLength
    
    def BuildCommand(self):
        temp = ''
        if self.GetOutputFolder() == None:
            return
        else:
            temp = temp + 'velvetg %s'% self.GetOutputFolder()
        if self.GetMinContigLength() != None:
            temp = temp + ' -min_contig_lgth %d'% self.GetMinContigLength()
        if self.GetMaxCov() != None:
            temp = temp + ' -max_coverage %d'% self.GetMaxCov()
        if self.GetCoverageCutoff() != None:
            temp = temp + ' -cov_cutoff %d'% self.GetCoverageCutoff()
        if self.GetExpCov() != None:
            temp = temp + ' -exp_cov %d'% self.GetExpCov()
        if self.GetInsertLength() != None:
            temp = temp + ' -ins_length %d'% self.GetInsertLength()
        return temp