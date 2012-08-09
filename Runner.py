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
    Strings = [MetaSimDir,MCONFDir,FastaFilesDir,ErrorModelsDir,DistributionModelsDir]
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
    ExpectedCoverages = [i for i in range(10,51,5)]
    KMER_Lengths = [75]
    NumOfReads = list()
    for i in FastaSizeList:
        for j in ExpectedCoverages:
            for k in KMER_Lengths:
                NumOfReads.append( i * j / k )
    return ExpectedCoverages, KMER_Lengths, NumOfReads, FastaSizeList, FastaFileList, FastaSequenceList, CurrentDirectory, Time

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

def MetaSimulator(MetaSimDir,InsertLengths,FastaFileList,ExpectedCoverages,KMER_Lengths,Sigma,FastaSequenceList,debug=None):
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
                            FastaSeqSize = len(FastaSequenceList[0].GetSeq())
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
                                      KMER_Length = KMER_Length,
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
                            MetaSimFiles = MetaSimDir + '*.fna'
                            SetOfFNAFiles = set(glob.glob(MetaSimFiles))
                            FNADifference = SetOfFNAFiles - FNAFileSet
                            FNAFile = FNADifference.pop()
                            VelvetCommander(FNAFile,INS,apple,ExpectedCoverage)
        return LincolnLog

def VelvetCommander(FNAFile,INS,apple,ExpectedCoverage):
    MinContigs = [50,300, 400, 500]
    
def VelvetSimulator(InsertsLengths,LincolnLog,Sigma,FastaSequenceList, Time, ExpectedCoverage, KMER_Lengths, debug=None): 
    pform = platform.uname()
    if 'Linux' in pform:
        Velveth = '/usr/local/bin/velveth'
        Velvetg = '/usr/local/bin/velvetg'
    else:
        Velveth = '/usr/local/genome/bin/velveth'
        Velvetg = '/usr/local/genome/bin/velvetg'
    #VelvetH
    """
    (Required) FileName      = None
    (Required) DirectoryName = None, the name of the directory to be created 
    HashLength      = 100, the kmer length
    FileFormat      ='fasta', 
    ReadType        ='shortPaired'
    """
    #from VelvetH import VelvetH
    FNA_List= glob.glob('MetaSimOutputs/*.fna')#find all files of this format and remove the time hash and .fna
    FNA_NameList= [ i[15:] for i in FNA_List]
    MinContigs = [50,300, 400, 500]
    VelvetHOutput = []
    """./velveth output_directory hash_length [[-file_format][-read_type] filename]
    1) make output directory from FNA_NameList, KMER, MinContig
    2) velveth
    """
    for i in range(len(FNA_List)):
        for j in range(len(KMER_Lengths)):
            for k in range(len(MinContigs)):
                for XP in range(len(ExpectedCoverage)):
                    for h,INS in enumerate(InsertsLengths):
                    """
                    DATE=`date +%m%d%H%M%S`
                    mkdir $1_KMER$2_CUT$3_EXP$4_CNTG$5
                    velveth $1_KMER$2_CUT$3_EXP$4_CNTG$5 $2 -fasta $6 &> $DATE_VH_$1_KMER$2_CUT$3_EXP$4_CNTG$5.log
                    mkdir  $DATE$1_KMER$2_CUT$3_EXP$4_CNTG$5
                    cd  $DATE$1_KMER$2_CUT$3_EXP$4_CNTG$5
                    ln -s ../$1_KMER$2_CUT$3_EXP$4_CNTG$5/Sequences
                    ln -s ../$1_KMER$2_CUT$3_EXP$4_CNTG$5/Roadmaps
                    cd ..
                    velvetg $DATE_$1_KMER$2_CUT$3_EXP$4_CNTG$5 -cov_cutoff $3 -exp_cov $4 -min_contig_lgth $5 &> $DATE_VG_$1_KMER$2_CUT$3_EXP$4_CNTG$5.log
                    """
                    #1)Make Directory
                    FolderName1 = CurrentDirectory + 'VelvetOutputs/%s-%dKMER-%dXC-%dMC'%(FNA_NameList[i],KMER_Lengths[j],ExpectedCoverage[XP],MinContigs[k])
                    if not debug:
                        if not os.path.exists(FolderName1):
                            VelvetFolderOutput = ['mkdir', FolderName1]
                            subprocess.call(VelvetFolderOutput,stdin=LincolnLog.InputLog,stderr=LincolnLog.ErrorLog,stdout=LincolnLog.OutputLog)
                            #VelvetH
                            FNAFile = CurrentDirectory + FNA_List[i]
                            VelvetHOutput = [Velveth, FolderName1, '%d' % KMER_Lengths[j], '-fasta', '-shortPaired', FNAFile] 
                            subprocess.call(VelvetHOutput,stdin=LincolnLog.InputLog,stderr=LincolnLog.ErrorLog,stdout=LincolnLog.OutputLog)
                            #Make Directory with date
                            FolderName2 = CurrentDirectory + 'VelvetOutputs/%s-%s-%dKMER-%dXC-%dMC'%(Time,FNA_NameList[i],KMER_Lengths[j],ExpectedCoverage[XP],MinContigs[k])
                            VelvetFolderOutput = ['mkdir', FolderName2]
                            subprocess.call(VelvetFolderOutput,stdin=LincolnLog.InputLog,stderr=LincolnLog.ErrorLog,stdout=LincolnLog.OutputLog)
                            #Symbolic Link1
                            ActualSeq = FolderName1 + '/Sequences'
                            LinkedSeq = FolderName2 + '/Sequences'
                            SymbolicLink1 = ['ln', '-s', ActualSeq,LinkedSeq]
                            subprocess.call(SymbolicLink1,stdin=LincolnLog.InputLog,stderr=LincolnLog.ErrorLog,stdout=LincolnLog.OutputLog)
                            #Symbolic Link2
                            ActualRoadmaps = FolderName1 + '/Roadmaps'
                            LinkedRoadmaps = FolderName2 + '/Roadmaps'
                            SymbolicLink2 = ['ln', '-s', ActualRoadmaps,LinkedRoadmaps]
                            subprocess.call(SymbolicLink2,stdin=LincolnLog.InputLog,stderr=LincolnLog.ErrorLog,stdout=LincolnLog.OutputLog)
                            #VelvetG
                            ExpectedCov = ExpectedCoverage[XP]
                            Velvet = [Velvetg ,FolderName2, '-cov_cutoff', '4', '-exp_cov', '%d'%ExpectedCov, '-min_contig_lgth', '%d'%MinContigs[k]]
                            subprocess.call(Velvet,stdin=LincolnLog.InputLog,stderr=LincolnLog.ErrorLog,stdout=LincolnLog.OutputLog)
                    else:
                        if not os.path.exists(FolderName1):
                            NameL,KM,EC,MC, FNAFile = FNA_NameList[i],KMER_Lengths[j],ExpectedCoverage[XP],MinContigs[k], CurrentDirectory + FNA_List[i]
                            FolderName2             = CurrentDirectory + 'VelvetOutputs/%s-%s-%dKMER-%dXC-%dMC'%(Time,NameL,KM,EC,MC)
                            ActualSeq               = FolderName1 + '/Sequences'
                            LinkedSeq               = FolderName2 + '/Sequences'
                            ActualRoadmaps          = FolderName1 + '/Roadmaps'
                            LinkedRoadmaps          = FolderName2 + '/Roadmaps'
                            FolderOutput1           = 'mkdir %s'%FolderName1
                            FolderOutput2           = 'mkdir %s'%FolderName2
                            VelvetHOutput           = '%s %s %d -fasta -shortPaired %s'%(Velveth, FolderName1,KM,FNAFile)
                            SymbolicLink1           = 'ln -s %s %s'%(ActualSeq,LinkedSeq)
                            SymbolicLink2           = 'ln -s %s %s'%(ActualRoadmaps,LinkedRoadmaps)
                            VelvetGOutput           = '%s %s -cov_cutoff 4 -exp_cov %d -min_contig_lgth %d'%(Velvetg,FolderName2,EC,MC)
                            os.system(FolderOutput1)
                            os.system(FolderOutput2)
                            os.system(VelvetHOutput)
                            os.system(SymbolicLink1)
                            os.system(SymbolicLink2)
                            os.system(VelvetGOutput)
    LincolnLog.ErrorLog.close()
    LincolnLog.InputLog.close()
    LincolnLog.OutputLog.close()

Velveth, Velvetg, MetaSimDir, MCONFDir, FastaFilesDir, ErrorModelsDir, DistributionModelsDir = SystemCheck()
ExpectedCoverages, KMER_Lengths, NumOfReads, FastaSizeList, FastaFileList, FastaSequenceList, CurrentDirectory, Time = FileReader()
MCONFBuilder(KMER_Lengths)
InsertsLengths = [300]
Sigma = SizeDistroBuilder(InsertsLengths,NumOfReads)
LincolnLog = MetaSimulator(MetaSimDir,InsertsLengths,FastaFileList,ExpectedCoverages,KMER_Lengths,Sigma,FastaSequenceList, debug=True) #If we really, really, really want to build new FNA Data, mark debug to false
VelvetSimulator(InsertsLengths,LincolnLog,Sigma,FastaSequenceList, Time,ExpectedCoverages,KMER_Lengths,debug=False) #if we really really want to use the subprocess.call, mark debug to false
