from FastaSequence import *
from ErrorModelMaker import ErrorModelMaker
from DistributionMaker import SizeDistribution
from MetasimPy import MetasimPy
from Logger import Logger
import glob, FastaSequence, os, subprocess, datetime, platform, sets

def SystemCheck():
    CurrentDirectory = os.getcwd() + '/'
    MetaSimDir = CurrentDirectory + 'MetaSimOutputs'
    MCONFDir = CurrentDirectory + 'MCONF'
    FastaFilesDir = CurrentDirectory + 'FastaFiles'
    ErrorModelsDir = CurrentDirectory + 'ErrorModels'
    DistributionModelsDir = CurrentDirectory + 'DistributionModels'
    VelvetDir = CurrentDirectory + 'VelvetOutputs'
    Logs = CurrentDirectory + 'LogFiles'
    Strings = [Logs,VelvetDir,MetaSimDir,MCONFDir,FastaFilesDir,ErrorModelsDir,DistributionModelsDir]
    for text in Strings:
        if not os.path.isdir(text):
            os.system('mkdir '+text)
    #check velvet Installation
    pform = platform.uname()
    if 'Linux' in pform:
        Velveth = '/usr/local/bin/velveth'
        Velvetg = '/usr/local/bin/velvetg'
    else:
        Velveth = '/usr/local/genome/bin/velveth'
        Velvetg = '/usr/local/genome/bin/velvetg'
    return Velveth, Velvetg, MetaSimDir, MCONFDir, FastaFilesDir, ErrorModelsDir, DistributionModelsDir

def FileReader():
    CurrentDirectory = os.getcwd() + '/'
    now = datetime.datetime.now()
    Time = [ now.year, now.month, now.day, now.hour, now.minute,now.second]
    Time = ''.join([str(i) for i in Time])
    """1) read all the fasta files, determine the size of the data"""
    FastaFileList = glob.glob('FastaFiles/*.fasta') #find all files of this format
    FastaSizeList = list()
    for filename in FastaFileList:
        FastaSequenceList = fasta_read(filename)
        FastaSizeList.append(len(FastaSequenceList[0].GetSeq()))
    ExpectedCoverages = [i for i in range(30,51,5)]
    KMER_Lengths = [75]
    NumOfReads = list()
    for i in FastaSizeList:
        for j in ExpectedCoverages:
            for k in KMER_Lengths:
                NumOfReads.append( i * j / k )
    return ExpectedCoverages, KMER_Lengths, NumOfReads, FastaSizeList, FastaFileList, CurrentDirectory, Time

def MCONFBuilder(KMER_Lengths):
    #Build Error Model
    #Need to develop Error File Name
    for i in KMER_Lengths:
        FileName1 = "ErrorModels/ErrorModel-%d-bp.mconf"%i
        FileName2 = "ErrorModels/ModifiedErrorModel-%d-bp.mconf"%i
        #FileName1 = "ErrorModels/EMTest-%d-bp.mconf"%i
        #FileName2 = "ErrorModels/VaryEMTest-%d-bp.mconf"%i
        BasicError = ErrorModelMaker(FileName = FileName1,N=i)
        VaryError = ErrorModelMaker(Variation = True, FileName=FileName2)

def SizeDistroBuilder(KMER_Lengths,NumOfReads):
    #SizeDistribution
    """
            Inputs:
            Mean = the average length of DNA Segments (integer)
            Sigma = the standard deviation of the DNA Segments (integer)
            NumOfReads = Number or reads for the distribution
            Objective of class: return a distribution file
    """
    Sigma = [i for i in range(8,15)]
    Mean = KMER_Lengths
    for i in Sigma:
        for j in Mean:
            for k in NumOfReads:
                FileName = "DistributionModels/DistributionModel%dSig%dMu%dNOR.txt"%(i,j,k)
                SizeDistribution(Sigma = i, Mean = j, NumOfReads = k,FileName=FileName)
    return Sigma

def MetaSimulator(Time,MetaSimDir,InsertLengths,FastaFileList,ExpectedCoverages,KMER_Lengths,Sigma,debug=None):
    #MetaSimpy
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
    LincolnLog = Logger()
    LincolnLog.BuildLogFiles()
#    Needs to do the following
#    for each fasta file, for each expected coverage, for each mean, for each sigma:
#    1)Get the number of reads from files
#    2)set metasimpy settings
    CurrentWorkingDirectory = os.getcwd()
    FNAFileSet = set(list())
    Dbug = debug
    if Dbug:
        return LincolnLog
    else:
        for filename in FastaFileList:
            for X in ExpectedCoverages:
                for K in KMER_Lengths:
                    for apple in Sigma:
                        for INS in InsertLengths:
                            """
                            for i in FastaSizeList:
                                for j in ExpectedCoverages:
                                    for k in KMER_Lengths:
                                        NumOfReads.append( i * j / k )
                            """
                            FastaSeq = fasta_read(filename)
                            FastaSeqSize = len(FastaSeq[0].GetSeq())
                            NOR = FastaSeqSize * X / K  #Number of Reads
                            KMER_Length = K
                            ErrorModel = "ErrorModels/ErrorModel-%d-bp.mconf"%K
                            #ErrorModel = "ErrorModels/EMTest-%d-bp.mconf"%K
                            FirstReadFile = ErrorModel
                            SecondReadFile = ErrorModel
                            EmpiricalPEProbability = 100
                            EmpiricalRead1Mid2End = True
                            EmpiricalRead2Mid2End = True
                            FastaFile = filename
                            ExpectedCoverage = X
                            Mean = K
                            InsertLengthDistribution = "DistributionModels/DistributionModel%dSig%dMu%dNOR.txt"%(apple,INS,NOR)
                            OutputDir = CurrentWorkingDirectory + '/MetaSimOutputs' 
                            MetasimPy(OutputDirectory=OutputDir,
                                      LogObject = LincolnLog, 
                                      KMER_Length = KMER_Length                         ,
                                      FirstReadFile = FirstReadFile,
                                      SecondReadFile = SecondReadFile,
                                      EmpiricalPEProbability = EmpiricalPEProbability,
                                      EmpiricalRead1Mid2End = EmpiricalRead1Mid2End,
                                      EmpiricalRead2Mid2End = EmpiricalRead2Mid2End,
                                      FastaFile = FastaFile,
                                      ExpectedCoverage = ExpectedCoverage,
                                      Mean = Mean,
                                      Sigma = apple,
                                      FragmentDistribution = InsertLengthDistribution,
                                      NumOfReads = NOR)
                            #Find the corresponding FNA File made by MetasimPy command
                            MetaSimFiles = MetaSimDir+ '/' + '*.fna'
                            SetOfFNAFiles = set(glob.glob(MetaSimFiles))
                            FNADifference = SetOfFNAFiles - FNAFileSet
                            FNAFile = FNADifference.pop()
                            VelvetCommander(31,Time,FNAFile,INS,apple,ExpectedCoverage,LincolnLog)
        return LincolnLog

def VelvetCommander(K,Time,FNAFile,INS,apple,ExpectedCoverage,LincolnLog):
    CurrentDirectory = os.getcwd() + '/'
    FullName = FNAFile
    Splits = os.path.split(FNAFile)
    FNADirectory = Splits[0]
    FNAFile = Splits[1]
    MinContigs = [100, 300, 400, 500]
    CovCutoff  = [4,5,6]
    for i,MC in enumerate(MinContigs):
        for j,CC in enumerate(CovCutoff):
            FolderName1             = CurrentDirectory + 'VelvetOutputs/%s-%dKMER-%dXC-%dMC-%dCC-%dINS-%dSig'%(FNAFile[0:-4],K,ExpectedCoverage,MC,CC,INS,apple)
            FolderName2             = CurrentDirectory + 'VelvetOutputs/%s-%s-%dKMER-%dXC-%dMC-%dCC-%dINS-%dSig'%(Time,FNAFile[0:-4],K,ExpectedCoverage,MC,CC,INS,apple)
            ActualSeq               = FolderName1 + '/Sequences'
            LinkedSeq               = FolderName2 + '/Sequences'
            ActualRoadmaps          = FolderName1 + '/Roadmaps'
            LinkedRoadmaps          = FolderName2 + '/Roadmaps'
            FolderOutput1           = ['mkdir', '%s'%FolderName1]
            FolderOutput2           = ['mkdir', '%s'%FolderName2]
            VelvetHOutput           = [Velveth, FolderName1,str(K), '-fasta', '-shortPaired', FullName]
            SymbolicLink1           = ['ln' ,'-s', ActualSeq,LinkedSeq]
            SymbolicLink2           = ['ln' ,'-s',ActualRoadmaps,LinkedRoadmaps]
            #VelvetGOutput          = '%s %s -cov_cutoff 4 -exp_cov %d -min_contig_lgth %d'%(Velvetg,FolderName2,EC,MC)
            VelvetGOutput           = [Velvetg, FolderName2,'-cov_cutoff',str(CC),'-exp_cov',str(ExpectedCoverage),'-min_contig_lgth',str(MC),'-ins_length',str(INS), '-ins_length_sd',str(apple)]
            CommandList             = [FolderOutput1,FolderOutput2,VelvetHOutput,SymbolicLink1,SymbolicLink2,VelvetGOutput]
            for C in CommandList:
                subprocess.call(C, stderr=LincolnLog.ErrorLog, stdout=LincolnLog.InputLog, stdin=LincolnLog.InputLog)
            


Velveth, Velvetg, MetaSimDir, MCONFDir, FastaFilesDir, ErrorModelsDir, DistributionModelsDir = SystemCheck()
ExpectedCoverages, KMER_Lengths, NumOfReads, FastaSizeList, FastaFileList, CurrentDirectory, Time = FileReader()
MCONFBuilder(KMER_Lengths)
InsertsLengths = [300]
Sigma = SizeDistroBuilder(InsertsLengths,NumOfReads)
LincolnLog = MetaSimulator(Time,MetaSimDir,InsertsLengths,FastaFileList,ExpectedCoverages,KMER_Lengths,Sigma, debug=False) #If we really, really, really want to build new FNA Data, mark debug to false
LincolnLog.ErrorLog.close()
LincolnLog.InputLog.close()
LincolnLog.OutputLog.close()