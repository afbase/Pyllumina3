import multiprocessing, subprocess, os
from FastaSequence import fasta_read
from Logger import Logger
class MetasimPy:
    CurrentDirectory = os.getcwd()
    DEBUG = True
    def __init__(self,OutputDirectory = 'MetaSimOutputs', LogObject = None, KMER_Length = 100, FirstReadFile = None, SecondReadFile = None, EmpiricalPEProbability = 100, EmpiricalRead1Mid2End = True, EmpiricalRead2Mid2End = True, NumOfThreads = multiprocessing.cpu_count(), FastaFile = None, ExpectedCoverage=30, Mean = 100,Sigma = 10,FragmentDistribution = 'gaussian',NumOfReads = None ):
        """
        Inputs:
        LogObject = a Logger class that is specified.
        KMER_Length = an integer
        FirstReadFile = Specify an empirical error  model config file
        SecondReadFile = Specify an empirical error  model config file for the 2nd read.
        EmpiricalPEProbability = Specify paired end probability for the  empirical error model.
        EmpiricalRead1Mid2End = read  #1 ends  at insert  end for  the  empirical error model.
        EmpiricalRead2Mid2End = read  #2 ends  at insert  end for  the  empirical error model.
        NumOfThreads = Set number of readsim threads
        FastaFile = fasta file or list of Fasta files (string or list of strings filenames respectively)
        ExpectedCoverage = the mean of the number of times a base pair is expected to be found in the total number of DNA segments (integer)
        Mean = the average length of DNA Segments (integer)
        Sigma = the standard deviation of the DNA Segments (integer)
        FragmenDistribution = 'gaussian' by default or 'uniform' or filename (filename implies empirical)
        NumOfReads = Numbers of reads or base pairs 
        """
        self.SetOutputDirectory(OutputDirectory)
        self.SetLogObject(LogObject)
        self.SetFragmentDistribution(FragmentDistribution)
        self.SetMean(Mean)
        self.SetSigma(Sigma)
        self.SetFirstReadFile(FirstReadFile)
        self.SetSecondReadFile(SecondReadFile)
        self.SetEmpiricalPEProbability(EmpiricalPEProbability)
        self.SetEmpiricalRead1Mid2End(EmpiricalRead1Mid2End)
        self.SetEmpiricalRead2Mid2End(EmpiricalRead2Mid2End)
        self.SetNumOfThreads(NumOfThreads)
        self.SetFastaFile(FastaFile)
        self.SetKMER_Length(KMER_Length)
        self.SetExpectedCoverage(ExpectedCoverage)
        self.SetNumOfReads(Num = NumOfReads)
        self.BuildOptionalStatement()
        self.RunStatement()
        
    def SetOutputDirectory(self,OD):
        self.OutputDirectory = OD
        if type(OD) == str:
            if OD[0] == '/':
                self.OutputDirectory = OD
            else:
                self.OutputDirectory = self.CurrentDirectory + '/' + OD #Change relative file location to exact file location
        else:
            self.OutputDirectory = OD
    def SetLogObject(self,LogObject):
        self.LogObject = LogObject
    def SetFragmentDistribution(self, FD):
        if type(FD) == str:
            if FD[0] == '/':
                self.FragmentDistribution = FD
            else:
                self.FragmentDistribution = self.CurrentDirectory + '/' + FD #Change relative file location to exact file location
        else:
            self.FragmentDistribution = FD
        #self.FragmentDistribution = FD
    def SetMean(self,AVG):
        self.Mean = AVG
    def SetSigma(self,Sigma):
        self.Sigma = Sigma
    def SetExpectedCoverage(self,ExpectedCoverage):
        self.ExpectedCoverage = ExpectedCoverage
    def SetKMER_Length(self,KMER_Length):
        self.KMER_Length = KMER_Length
    def SetFirstReadFile(self,FirstReadFile):
        if FirstReadFile[0] == '/':
            self.FirstReadFile = FirstReadFile
        else:
            self.FirstReadFile = self.CurrentDirectory + '/' + FirstReadFile #Change relative file location to exact file location
    def SetSecondReadFile(self,SecondReadFile):
        if SecondReadFile[0] == '/':
            self.SecondReadFile = SecondReadFile
        else:
            self.SecondReadFile = self.CurrentDirectory + '/' + SecondReadFile #Change relative file location to exact file location
    def SetEmpiricalPEProbability(self,EmpiricalPEProbability):
        self.EmpiricalPEProbability = EmpiricalPEProbability
    def SetEmpiricalRead1Mid2End(self,EmpiricalRead1Mid2End):
        self.EmpiricalRead1Mid2End = EmpiricalRead1Mid2End
    def SetEmpiricalRead2Mid2End(self,EmpiricalRead2Mid2End):
        self.EmpiricalRead2Mid2End = EmpiricalRead2Mid2End
    def SetNumOfThreads(self,NumOfThreads):
        self.NumOfThreads = NumOfThreads
    def SetFastaFile(self,FastaFile):
        if FastaFile[0] == '/':
            self.FastaFile = FastaFile
        else:
            self.FastaFile = self.CurrentDirectory + '/' + FastaFile #Change relative file location to exact file location
    def SetFastaSequence(self,Seq):
        self.FastaSequence = Seq
    def SetMetaSimCommand(self,command):
        self.MetaSimCommand = command
    def SetNumOfReads(self, Num = None):
        if Num == None:
            FastaSeq = fasta_read(self.GetFastaFile())
            SeqObj = FastaSeq[0].GetSequence()
            SeqObjLen = len(SeqObj)
            self.NumOfReads = SeqObjLen*self.GetExpectedCoverage()/self.GetKMER_Length()
        else:
            self.NumOfReads = Num

    def GetFragmentDistribution(self):
        return self.FragmentDistribution
    def GetMean(self):
        return self.Mean
    def GetSigma(self):
        return self.Sigma
    def GetExpectedCoverage(self):
        return self.ExpectedCoverage
    def GetKMER_Length(self):
        return self.KMER_Length
    def GetFirstReadFile(self):
        return self.FirstReadFile
    def GetSecondReadFile(self):
        return self.SecondReadFile
    def GetEmpiricalPEProbability(self):
        return self.EmpiricalPEProbability
    def GetEmpiricalRead1Mid2End(self):
        return self.EmpiricalRead1Mid2End
    def GetEmpiricalRead2Mid2End(self):
        return self.EmpiricalRead2Mid2End
    def GetNumOfThreads(self):
        return self.NumOfThreads
    def GetFastaFile(self):
        return self.FastaFile
    def GetFastaSequence(self):
        return self.FastaSequence
    def GetNumOfReads(self):
        return self.NumOfReads
    def GetMetaSimCommand(self):
        return self.MetaSimCommand
    def GetLogObject(self):
        return self.LogObject
    def GetOutputDirectory(self):
        return self.OutputDirectory
       
    def BuildOptionalStatement(self):
        """
        Inputs:
        KMER_Length = an integer
        -------------------FirstReadFile = Specify an empirical error  model config file
        SecondReadFile = Specify an empirical error  model config file for the 2nd read.
        EmpiricalPEProbability = Specify paired end probability for the  empirical error model.
        EmpiricalRead1Mid2End = read  #1 ends  at insert  end for  the  empirical error model.
        EmpiricalRead2Mid2End = read  #2 ends  at insert  end for  the  empirical error model.
        NumOfThreads = Set number of readsim threads
        FastaFile = fasta file or list of Fasta files (string or list of strings filenames respectively)
        ExpectedCoverage = the mean of the number of times a base pair is expected to be found in the total number of DNA segments (integer)
        ----------------Mean = the average length of DNA Segments (integer)
        Sigma = the standard deviation of the DNA Segments (integer)
        FragmenDistribution = 'gaussian' or 'uniform'
        """
        """
        Order of inputs
        1) Number of reads
        2) empirical/solexa error model
        3) Specify an empirical error model config file mconf
        4) Specify an empirical error model config file for the 2nd read.
        5) --empirical-pe-probability 100 
        6) -f Mean Value
        7) -t stddev 
        8) Fast File
        """
        Options = ['MetaSim', 'cmd']
        #1) Number of reads
        Options.append('-r')
        Options.append(str(self.GetNumOfReads()))
        #2) empirical/solexa error model
        Options.append('-m')
        #3) Specify an empirical error model config file mconf
        Options.append('-g')
        Options.append(str(self.GetFirstReadFile()))
        #4) Specify an empirical error model config file for the 2nd read.
        #5) --empirical-pe-probability 100 
        if self.GetSecondReadFile() != None:
            #Options += '-2 %s '%self.GetSecondReadFile()
            Options.append('-2')
            Options.append(self.GetSecondReadFile())
            #Options += '--empirical-pe-probability %d '%self.GetEmpiricalPEProbability()
            Options.append('--empirical-pe-probability')
            Options.append(str(self.GetEmpiricalPEProbability()))
        #6) -f Mean Value
        Options.append('-f')
        Options.append(str(self.GetKMER_Length()))
        #7) -t stddev
        Options.append('-t')
        Options.append(str(self.GetSigma()))
        #7.5) Set output Directory
        Options.append('-d')
        Options.append(self.GetOutputDirectory())
        #8)  Set Distribution Size
        Options.append('-w')
        Options.append(self.GetFragmentDistribution()) 
        #8.5) Fast File
        Options.append(self.GetFastaFile()) 
        #9) Set  commands
        self.SetMetaSimCommand(Options)     
          
#        if self.GetEmpiricalRead1Mid2End():
#            #Options += '--empirical-read1-mid2end '
#            Options.append('--empirical-read1-mid2end')
#        if self.GetEmpiricalRead2Mid2End():
#            #Options += '--empirical-read2-mid2end '
#            Options.append('--empirical-read2-mid2end')
#        #Options += '--threads %s '%self.GetNumOfThreads()
#        Options.append('--threads')
#        Options.append(str(self.GetNumOfThreads()))
#        if self.GetFragmentDistribution() == 'uniform':
#            #Options += '-v '
#            Options.append('-v')
#        elif self.GetFragmentDistribution()== 'gaussian':
#            self.SetFragmentDistribution(self.GetFragmentDistribution())
#        else:
#            #Options += '-w %s '%self.GetFragmentDistribution()
#            Options.append('-w')
#            Options.append(self.GetFragmentDistribution())
#        #OutputDirectory
#        Options.append
#        Options.append(self.GetOutputDirectory())

        
        
        
#        Options  = 'MetaSim cmd -m '
#        """
#        1) Number of Reads
#        2) KMER Length
#        3) sigma
#        4) Fasta File
#        5) check Second Fasta File
#        6) PePprobability
#        7) Check Read1 mid2end & check Read2 mid2end
#        8) NumOfThreads
#        9) FragmentDistribution
#        """
#        Options += '-r %s '%self.GetNumOfReads()
#        Options += '-f %d '%self.GetKMER_Length()
#        Options += '-t %d '%self.GetSigma()
#        Options += '-g %s '%self.GetFirstReadFile()
#        if self.GetSecondReadFile() != None:
#            Options += '-2 %s '%self.GetSecondReadFile()
#            Options += '--empirical-pe-probability %d '%self.GetEmpiricalPEProbability()
#        if self.GetEmpiricalRead1Mid2End():
#            Options += '--empirical-read1-mid2end '
#        if self.GetEmpiricalRead2Mid2End():
#            Options += '--empirical-read2-mid2end '
#        Options += '--threads %s '%self.GetNumOfThreads()
#        if self.GetFragmentDistribution() == 'uniform':
#            Options += '-v '
#        elif self.GetFragmentDistribution()== 'gaussian':
#            self.SetFragmentDistribution(self.GetFragmentDistribution())
#        else:
#            Options += '-w %s '%self.GetFragmentDistribution()
#        Options += '%s'%self.GetFastaFile()
#        self.SetMetaSimCommand(Options)
    
    def RunStatement(self):
        if self.DEBUG:
            #make a space between each element of the list of metasim commands
            Commands = self.GetMetaSimCommand()
            j = ''
            for i in range(len(Commands)):
                Commands[i] = Commands[i] + ' '
                j = j + Commands[i]
            self.SetMetaSimCommand(j)
            os.system(self.GetMetaSimCommand()) 
        else:
            if self.GetLogObject() == None:
                Logr = Logger()
                Logr.BuildLogFiles()
            else:
                Logr = self.GetLogObject()
            subprocess.call(self.GetMetaSimCommand(),stdin=Logr.InputLog,stderr=Logr.ErrorLog,stdout=Logr.OutputLog)
            