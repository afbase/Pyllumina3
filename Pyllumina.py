import multiprocessing
from FastaSequence import fasta_read
class Pyllumina:
    def __init__(self, KMER_Length = 100, FirstReadFile = None, SecondReadFile = None, EmpiricalPEProbability = 100, EmpiricalRead1Mid2End = None, EmpiricalRead2Mid2End = None, NumOfThreads = multiprocessing.cpu_count(), FastaFile = None, ExpectedCoverage=30, Mean = 100,Sigma = 10,FragmentDistribution = 'gaussian' ):
        """
        Inputs:
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
        FragmenDistribution = 'gaussian' or 'uniform'
        """
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
        self.SetNumOfReads()
        self.BuildOptionalStatements()
        
    def SetFragmentDistribution(self, FD):
        self.FragmentDistribution = FD
    def SetMean(self,AVG):
        self.Mean = AVG
    def SetSigma(self,Sigma):
        self.Sigma = Sigma
    def SetExpectedCoverage(self,ExpectedCoverage):
        self.ExpectedCoverage = ExpectedCoverage
    def SetKMER_Length(self,KMER_Length):
        KMER_Length = KMER_Length
    def SetFirstReadFile(self,FirstReadFile):
        self.FirstReadFile = FirstReadFile
    def SetSecondReadFile(self,SecondReadFile):
        self.SecondReadFile = SecondReadFile
    def SetEmpiricalPEProbability(self,EmpiricalPEProbability):
        self.EmpiricalPEProbability = EmpiricalPEProbability
    def SetEmpiricalRead1Mid2End(self,EmpiricalRead1Mid2End):
        self.EmpiricalRead1Mid2End = EmpiricalRead1Mid2End
    def SetEmpiricalRead2Mid2End(self,EmpiricalRead2Mid2End):
        self.EmpiricalRead2Mid2End = EmpiricalRead2Mid2End
    def SetNumOfThreads(self,NumOfThreads):
        self.NumOfThreads = NumOfThreads
    def SetFastaFile(self,FastaFile):
        self.FastaFile = FastaFile
    def SetFastaSequence(self,Seq):
        self.FastaSequence = Seq
    def SetNumOfReads(self,Quantity):
        self.NumOfReads = Quantity
        
    def GetFragmentDistribution(self):
        return self.FragementDistribution
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
    
    def SetNumOfReads(self):
        FastaSeq = fasta_read(self.GetFastaFile())
        SeqObj = FastaSeq[0].GetSequence()
        SeqObjLen = len(SeqObj)
        self.SetNumOfReads(SeqObjLen*self.GetExpectedCoverage()/self.GetKMER_Length())
    def CollectOptionalStatement(self):
        
