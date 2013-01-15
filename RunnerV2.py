from FastaSequence import *
from ErrorModelMaker import ErrorModelMaker
from DistributionMaker import SizeDistribution
from MetasimPy import MetasimPy
from Logger import Logger
import glob, FastaSequence, os, subprocess, datetime, platform, re, shutil

def SystemCheck():
    CurrentDirectory = os.getcwd() + '/'
    VelvetAnalysisDir = CurrentDirectory + 'VelvetAnalysis'
    MetaSimDir = CurrentDirectory + 'MetaSimOutputs'
    MCONFDir = CurrentDirectory + 'MCONF'
    FastaFilesDir = CurrentDirectory + 'FastaFiles'
    ErrorModelsDir = CurrentDirectory + 'ErrorModels'
    DistributionModelsDir = CurrentDirectory + 'DistributionModels'
    VelvetDir = CurrentDirectory + 'VelvetOutputs'
    Logs = CurrentDirectory + 'LogFiles'
    Strings = [Logs,VelvetAnalysisDir , VelvetDir,MetaSimDir,MCONFDir,FastaFilesDir,ErrorModelsDir,DistributionModelsDir]
    for text in Strings:
        if not os.path.isdir(text):
            os.system('mkdir '+text)
    #check velvet Installation
    pform = platform.uname()
    if 'Linux' in pform:
        Velveth = '/usr/bin/velveth'
        Velvetg = '/usr/bin/velvetg'
    else:
        Velveth = '/usr/local/genome/bin/velveth'
        Velvetg = '/usr/local/genome/bin/velvetg'
    return VelvetAnalysisDir, Velveth, Velvetg, MetaSimDir, MCONFDir, FastaFilesDir, ErrorModelsDir, DistributionModelsDir

def FileReader(FileDirectory):
    CurrentDirectory = os.getcwd() + '/'
    now = datetime.datetime.now()
    Time = [ now.year, now.month, now.day, now.hour, now.minute,now.second]
    Time = ''.join([str(i) for i in Time])
    """1) read all the fasta files, determine the size of the data"""
    FastaFileList = glob.glob(FileDirectory + '/*.fasta') #find all files of this format
    FastaSizeList = list()
    for filename in FastaFileList:
        FastaSequenceList = fasta_read(filename)
        FastaSizeList.append(len(FastaSequenceList[0].GetSeq()))
#    ExpectedCoverages = [i for i in range(30,51,5)]
    ExpectedCoverages = [300]#[400,500,600,350]
    KMER_Lengths = [75]
    NumOfReads = list()
    for i in FastaSizeList:
        for j in ExpectedCoverages:
            for k in KMER_Lengths:
                NumOfReads.append( i * j / k )
    return ExpectedCoverages, KMER_Lengths, NumOfReads, FastaSizeList, FastaFileList, CurrentDirectory, Time

def MergeFastaFiles(FileList,concatenatedName):
    destination = open(concatenatedName,'wb')
    for i,fileName in enumerate(FileList):
        shutil.copyfileobj(open(fileName,'rb'), destination)
    destination.close()

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

def SizeDistroBuilder(INSlength,NumOfReads):
    #SizeDistribution
    """
            Inputs:
            INSlength = the average length of space between pairs of DNA Segments (integer)
            Sigma = the standard deviation of the DNA Segments (integer)
            NumOfReads = Number or reads for the distribution
            Objective of class: return a distribution file
    """
    Sigma = [1,3]#[1,9,11,13,6]
    Mean = INSlength
    for i in Sigma:
        for j in Mean:
            for k in NumOfReads:
                FileName = "DistributionModels/DistributionModel%dSig%dMu%dNOR.txt"%(i,j,k)
                SizeDistribution(Sigma = i, Mean = j, NumOfReads = k,FileName=FileName)
    return Sigma

def MetaSimulator(VelvetAnalysisDir,Time,MetaSimDir,InsertLengths,FastaFileList,ExpectedCoverages,KMER_Lengths,Sigma,debug=None):
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
    MetaSimFilesGlob = MetaSimDir + '\*.fna'
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
        for INS in InsertLengths:
            for X in ExpectedCoverages:
                for K in KMER_Lengths:
                    for apple in Sigma:
                        #Build a directory of Files in the metasimoutputs directory.
                        FNAFileSet = set(glob.glob(MetaSimFilesGlob))
                        for filename in FastaFileList:
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
                            MetasimPy(Mean = K,
                                      OutputDirectory=OutputDir,
                                      LogObject = LincolnLog, 
                                      KMER_Length = KMER_Length                         ,
                                      FirstReadFile = FirstReadFile,
                                      SecondReadFile = SecondReadFile,
                                      EmpiricalPEProbability = EmpiricalPEProbability,
                                      EmpiricalRead1Mid2End = EmpiricalRead1Mid2End,
                                      EmpiricalRead2Mid2End = EmpiricalRead2Mid2End,
                                      FastaFile = FastaFile,
                                      ExpectedCoverage = ExpectedCoverage,
                                      Sigma = apple,
                                      FragmentDistribution = InsertLengthDistribution,
                                      NumOfReads = NOR)
                        #Needs to concatenate the corresponding Fasta Files.
                        MetaSimFiles = MetaSimDir+ '/' + '*.fna'
                        SetOfFNAFiles = set(glob.glob(MetaSimFiles))
                        FNADifference = list(SetOfFNAFiles - FNAFileSet)
                        ConcatenatedFilename=''.join([MetaSimDir,'/','INS',str(INS),'EXP',str(X),'KMER',str(K),'SIGMA',str(apple),'.fna'])
                        MergeFastaFiles(FNADifference, ConcatenatedFilename)
                        VelvetCommander(31,Time,ConcatenatedFilename,INS,apple,ExpectedCoverage,LincolnLog)
                        VelvetAnalysis(filename,VelvetAnalysisDir)#This needs to be redone
        return LincolnLog
def VelvetAnalysis(FileName, VelvetAnalysisDir):
    """
    1)  Composite Velvet analysis takes all parameters (input and output params and puts them together
    2)  Individual Analysis makes a table of inputs as rows and outputs as columns
    """
    CurrentDirectory = os.getcwd()
    DataVectors = list()
    Path,FNAname = os.path.split(FileName)
    SpeciesName = FNAname[0:-4]
    SpeciesLog = VelvetAnalysisDir+'/'+SpeciesName+'Analysis'
    AnalysisFilePtr = open(SpeciesLog,'w')
    AnalysisFilePtr.write('largest Contig, n50, Total Contig Length, KMER, Expected Covereage, Minimum Contig, Coverage Cutoff, Insert Pair Length, Insert Pair Sigma, Scaffolding,Final Graph Node count, used reads, total reads, Final Graph has X Nodes\n')
    BasePath = CurrentDirectory
    VelvetLogOutputs= BasePath + '/VelvetOutputs/*' + SpeciesName + '*/Log'
    SpecieLogs = glob.glob(VelvetLogOutputs)
    for i,Fname in enumerate(SpecieLogs):
        #31KMER-35XC-500MC-4CC-300INS-9Sig
        VelvetParams = re.findall('(\d+)KMER-(\d+)XC-(\d+)MC-(\d+)CC-(\d+)INS-(\d+)Sig-(\w+)_SCAFF',Fname)
        if len(VelvetParams)>0:
            KMER,ExpectedCoverage,MinContig,CoverageCutoff,Insertlength,InsSigma,Scaffolding = VelvetParams[0][0], VelvetParams[0][1], VelvetParams[0][2], VelvetParams[0][3], VelvetParams[0][4], VelvetParams[0][5], VelvetParams[0][6]
            if Scaffolding == 'yes':
                Scaffolding = 1
            else:
                Scaffolding = 0  
        FilePtr = open(Fname,'r')
        Lines = FilePtr.readlines()
        FilePtr.close()
        if 'Final graph' in Lines[-1]:
            M = re.findall('Final graph has (\d+) nodes and n50 of (\d+), max (\d+), total (\d+), using (\d+)/(\d+) reads', Lines[-1])
            M = M[0]
            #The data vectores should have largest contig, n50, tcl, velvet inputs, metasim inputs, etc.
            #DataVector:  largest Contig, n50, Total Contig Length, KMER, Expected Covereage, Minimum Contig, Coverage Cutoff, Insert Pair Length, Insert Pair Sigma, Scaffolding, Final Graph Node count, used reads, total reads, Nodes 
            DataVectors.append((int(M[2]), int(M[1]), int(M[3]), int(KMER), int(ExpectedCoverage), int(MinContig), int(CoverageCutoff), int(Insertlength), int(InsSigma), Scaffolding, int(M[0]), int(M[4]), int(M[5]) ,       int(M[0])     ))
    DataVectors.sort(reverse=True)
    for K in DataVectors:
        AnalysisFilePtr.write('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n'%(K[0 ],K[1 ],K[2 ],K[3 ],K[4 ],K[5  ],K[6 ],K[7 ],K[8 ],K[9 ],K[10],K[11],K[12],K[13]))
    AnalysisFilePtr.close()
        
        

        
def VelvetCommander(K,Time,FNAFile,INS,apple,ExpectedCoverage,LincolnLog):
    CurrentDirectory = os.getcwd() + '/'
    FullName = FNAFile
    Splits = os.path.split(FNAFile)
    FNADirectory = Splits[0]
    FNAFile = Splits[1]
    MinContigs = [700]
    Scaffolding = ['yes','no']
    CovCutoff  = [10,20]
    for SC in Scaffolding:
        for K in [65,55]:
            for i,MC in enumerate(MinContigs):
                for j,CC in enumerate(CovCutoff):
                    FolderName1             = CurrentDirectory + 'VelvetOutputs/%s-%dKMER-%dXC-%dMC-%dCC-%dINS-%dSig-%s_SCAFF'%(FNAFile[0:-4],K,ExpectedCoverage,MC,CC,INS,apple,SC)
                    FolderName2             = CurrentDirectory + 'VelvetOutputs/%s-%s-%dKMER-%dXC-%dMC-%dCC-%dINS-%dSig-%s_SCAFF'%(Time,FNAFile[0:-4],K,ExpectedCoverage,MC,CC,INS,apple,SC)
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
                    VelvetGOutput           = [Velvetg, FolderName2,'-cov_cutoff',str(CC),'-exp_cov',str(ExpectedCoverage),'-min_contig_lgth',str(MC),'-ins_length',str(INS), '-ins_length_sd',str(apple), '-scaffolding', SC]
                    CommandList             = [FolderOutput1,FolderOutput2,VelvetHOutput,SymbolicLink1,SymbolicLink2,VelvetGOutput]
                    for C in CommandList:
                        subprocess.call(C, stderr=LincolnLog.ErrorLog, stdout=LincolnLog.InputLog, stdin=LincolnLog.InputLog)
                    


VelvetAnalysisDir,Velveth, Velvetg, MetaSimDir, MCONFDir, FastaFilesDir, ErrorModelsDir, DistributionModelsDir = SystemCheck()
ExpectedCoverages, KMER_Lengths, NumOfReads, FastaSizeList, FastaFileList, CurrentDirectory, Time = FileReader(FastaFilesDir)
MCONFBuilder(KMER_Lengths)
InsertsLengths = [300]
Sigma = SizeDistroBuilder(InsertsLengths,NumOfReads)
LincolnLog = MetaSimulator(VelvetAnalysisDir,Time,MetaSimDir,InsertsLengths,FastaFileList,ExpectedCoverages,KMER_Lengths,Sigma, debug=False) #If we really, really, really want to build new FNA Data, mark debug to false
LincolnLog.ErrorLog.close()
LincolnLog.InputLog.close()
LincolnLog.OutputLog.close()
#CurrentDirectory = os.getcwd() + '/'
#VelvetAnalysisDir = CurrentDirectory + 'VelvetAnalysis'
#Filename = 'FastaFiles/BorreliaBurgdorferiB31_CP32-3.fasta'
#VelvetAnalysis(Filename, VelvetAnalysisDir)