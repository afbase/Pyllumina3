from FastaSequence import *
from ErrorModelMaker import ErrorModelMaker
from DistributionMaker import SizeDistribution
from MetasimPy import MetasimPy
from Logger import Logger
import glob, FastaSequence, os, subprocess, datetime
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
        BasicError = ErrorModelMaker(FileName = FileName1)
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
    #Sigma.append(0)
    Mean = KMER_Lengths
    for i in Sigma:
        for j in Mean:
            for k in NumOfReads:
                FileName = "DistributionModels/DistributionModel%dSig%dMu%dNOR.txt"%(i,j,k)
                SizeDistribution(Sigma = i, Mean = j, NumOfReads = k,FileName=FileName)
    return Sigma

def MetaSimulator(FastaFileList,ExpectedCoverages,KMER_Lengths,Sigma,FastaSequenceList,debug=None):
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
    """
    Needs to do the following
    for each fasta file, for each expected coverage, for each mean, for each sigma:
    1)Get the number of reads from files
    2)set metasimpy settings
    3)hope for results
    """
    Dbug = debug or True
    if Dbug:
        return LincolnLog
    else:
        for filename in FastaFileList:
            for X in ExpectedCoverages:
                for K in KMER_Lengths:
                    for apple in Sigma:
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
                        FragmenDistribution = "DistributionModels/DistributionModel%dSig%dMu%dNOR.txt"%(apple,K,NOR)
                        MetasimPy(LogObject = LincolnLog, 
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
                                  FragmentDistribution = FragmenDistribution,
                                  NumOfReads = NOR)
        return LincolnLog

def VelvetSimulator(LincolnLog,Sigma,FastaSequenceList, Time,debug=None):
    Dbug = debug or False
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
    MinContigs = [300, 400, 500]
    VelvetHOutput = []
    ExpectedCoverage = [10]#TestingMode
    KMER_Lengths = [99]         #TestingMode
    """./velveth output_directory hash_length [[-file_format][-read_type] filename]
    1) make output directory from FNA_NameList, KMER, MinContig
    2) velveth
    """
    for i in range(len(FNA_List)):
        for j in range(len(KMER_Lengths)):
            for k in range(len(MinContigs)):
                for XP in range(len(ExpectedCoverage)):
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
                    if not Dbug:
                        if not os.path.exists(FolderName1):
                            VelvetFolderOutput = ['mkdir', FolderName1]
                            subprocess.call(VelvetFolderOutput,stdin=LincolnLog.InputLog,stderr=LincolnLog.ErrorLog,stdout=LincolnLog.OutputLog)
                            #VelvetH
                            FNAFile = CurrentDirectory + FNA_List[i]
                            VelvetHOutput = ['velveth', FolderName1, '%d'%KMER_Lengths[j], '-fasta', '-shortPaired', FNAFile] 
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
                            Velvet = ['velvetg',FolderName2, '-cov_cutoff', '4', '-exp_cov', '%d'%ExpectedCov, '-min_contig_lgth', '%d'%MinContigs[k]]
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
                            VelvetHOutput           = '/usr/local/genome/bin/velveth %s %d -fasta -shortPaired %s'%(FolderName1,KM,FNAFile)
                            SymbolicLink1           = 'ln -s %s %s'%(ActualSeq,LinkedSeq)
                            SymbolicLink2           = 'ln -s %s %s'%(ActualRoadmaps,LinkedRoadmaps)
                            VelvetGOutput           = '/usr/local/genome/bin/velvetg %s -cov_cutoff 4 -exp_cov %d -min_contig_lgth %d'%(FolderName2,EC,MC)
                            os.system(FolderOutput1)
                            os.system(FolderOutput2)
                            os.system(VelvetHOutput)
                            os.system(SymbolicLink1)
                            os.system(SymbolicLink2)
                            os.system(VelvetGOutput)
                            
                            
    ##VelvetG
    #"""
    #        (required) OutputFolder = Output Directory of DeBruijn Graph Results
    #        CoverageCutoff = Minimum amount of times a base pair is sequenced
    #        MinContigLength = The smallest continuous sequenced length output desired
    #        ExpCov = The expected coverage of times a base pair is sequenced 
    #        MaxCov = the largest amount of times a base pair is sequenced
    #        (requires pairs ends option in velveth) InsertLength =  To activate the use of read pairs, you must specify two parameters: the
    #                                                                expected (i.e. average) insert length (or at least a rough estimate), and the
    #                                                                expected short-read k-mer coverage (see 5.1 for more information)
    #"""
    #from VelvetG import VelvetG
    LincolnLog.ErrorLog.close()
    LincolnLog.InputLog.close()
    LincolnLog.OutputLog.close()

ExpectedCoverages, KMER_Lengths, NumOfReads, FastaSizeList, FastaFileList, FastaSequenceList, CurrentDirectory, Time = FileReader()
MCONFBuilder(KMER_Lengths)
Sigma = SizeDistroBuilder(KMER_Lengths,NumOfReads)
LincolnLog = MetaSimulator(FastaFileList,ExpectedCoverages,KMER_Lengths,Sigma,FastaSequenceList, debug=True) #If we really, really, really want to build new MCONF Data, mark debug to false
VelvetSimulator(LincolnLog,Sigma,FastaSequenceList, Time,debug=True) #if we really really want to use the subprocess.call, mark debug to false
