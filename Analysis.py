import glob, re, os
def VelvetAnalysis():
    """
    1)  Composite Velvet analysis takes all parameters (input and output params and puts them together
    2)  Individual Analysis makes a table of inputs as rows and outputs as columns
    """
    CurrentDirectory = os.getcwd()
    FastaCompositeFiles = CurrentDirectory + '/FastaComposites'
    VelvetAnalysisDir = CurrentDirectory + '/VelvetAnalysis'
    FastaFiles = glob.glob(FastaCompositeFiles + '/*.fasta')
    for j,FileName in enumerate(FastaFiles):
        DataVectors = list()
        Path,FNAname = os.path.split(FileName)
        SpeciesName = FNAname[0:-6]
        SpeciesLog = VelvetAnalysisDir+'/'+SpeciesName+'Analysis'
        AnalysisFilePtr = open(SpeciesLog,'w')
        AnalysisFilePtr.write('largest Contig, n50, Total Contig Length, KMER, Expected Covereage, Minimum Contig, Coverage Cutoff, Insert Pair Length, Insert Pair Sigma, Scaffolding,Final Graph Node count, used reads, total reads, Final Graph has X Nodes\n')
        BasePath = CurrentDirectory
        VelvetLogOutputs= BasePath + '/VelvetOutputs/*' + SpeciesName + '*/Log'
        SpecieLogs = glob.glob(VelvetLogOutputs)
        for i,Fname in enumerate(SpecieLogs):
            #31KMER-35XC-500MC-4CC-300INS-9Sig
            VelvetParams = re.findall('(\d+)KMER-(\d+)XC-(\d+)MC-(\d+)CC-(\d+)INS-(\d+)Sig',Fname)
            if len(VelvetParams)>0:
                KMER,ExpectedCoverage,MinContig,CoverageCutoff,Insertlength,InsSigma = VelvetParams[0][0], VelvetParams[0][1], VelvetParams[0][2], VelvetParams[0][3], VelvetParams[0][4], VelvetParams[0][5]  
            FilePtr = open(Fname,'r')
            Lines = FilePtr.readlines()
            FilePtr.close()
            if 'Final graph' in Lines[-1]:
                M = re.findall('Final graph has (\d+) nodes and n50 of (\d+), max (\d+), total (\d+), using (\d+)/(\d+) reads', Lines[-1])
                M = M[0]
                #The data vectores should have largest contig, n50, tcl, velvet inputs, metasim inputs, etc.
                #DataVector:  largest Contig, n50, Total Contig Length, KMER, Expected Covereage, Minimum Contig, Coverage Cutoff, Insert Pair Length, Insert Pair Sigma, Scaffolding, Final Graph Node count, used reads, total reads, Nodes 
                DataVectors.append((int(M[2]), int(M[1]), int(M[3]), int(KMER), int(ExpectedCoverage), int(MinContig), int(CoverageCutoff), int(Insertlength), int(InsSigma), 0, int(M[0]), int(M[4]), int(M[5]), int(M[0]) )              )
        DataVectors.sort(reverse=True)
        for K in DataVectors:
            AnalysisFilePtr.write('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n'%(K[0 ],K[1 ],K[2 ],K[3 ],K[4 ],K[5  ],K[6 ],K[7 ],K[8 ],K[9 ],K[10],K[11],K[12],K[13]))
        AnalysisFilePtr.close()
def VelvetCompositeAnalysis(FileName, VelvetAnalysisDir):
    """
    1)  Composite Velvet analysis takes all parameters (input and output params and puts them together
    2)  Individual Analysis makes a table of inputs as rows and outputs as columns
    """
    DataVectors = list()
    Path,FNAname = os.path.split(FileName)
    SpeciesName = FNAname[0:-6]
    SpeciesLog = VelvetAnalysisDir+'/'+SpeciesName+'Analysis'
    AnalysisFilePtr = open(SpeciesLog,'w')
    AnalysisFilePtr.write('MaxContigLength,KMER,ExpectedCoverage,MinContig,CoverageCutoff,Insertlength,InsSigma,Nodes,N50,Max,UsedReads,TotalReads\n')
    BasePath = Path[0:-11]
    VelvetLogOutputs= BasePath + 'VelvetOutputs/*' + SpeciesName + '*/Log'
    SpecieLogs = glob.glob(VelvetLogOutputs)
    for i,Fname in enumerate(SpecieLogs):
        #31KMER-35XC-500MC-4CC-300INS-9Sig
        VelvetParams = re.findall('(\d+)KMER-(\d+)XC-(\d+)MC-(\d+)CC-(\d+)INS-(\d+)Sig',Fname)
        if len(VelvetParams)>0:
            KMER,ExpectedCoverage,MinContig,CoverageCutoff,Insertlength,InsSigma = VelvetParams[0][0], VelvetParams[0][1], VelvetParams[0][2], VelvetParams[0][3], VelvetParams[0][4], VelvetParams[0][5]  
        FilePtr = open(Fname,'r')
        Lines = FilePtr.readlines()
        FilePtr.close()
        if 'Final graph' in Lines[-1]:
            M = re.findall('Final graph has (\d+) nodes and n50 of (\d+), max (\d+), total (\d+), using (\d+)/(\d+) reads', Lines[-1])
            M = M[0]
            #Max,KMER,ExpectedCoverage,MinContig,CoverageCutoff,Insertlength,InsSigma,Nodes,N50,Max,UsedReads,TotalReads
            DataVectors.append((int(M[2]),int(KMER),int(ExpectedCoverage),int(MinContig),int(CoverageCutoff),int(Insertlength),int(InsSigma),int(M[0]),int(M[1]),int(M[3]),int(M[4]),int(M[5])))
            #AnalysisFilePtr.write(Fname + '\n')
    DataVectors.sort(reverse=True)
    for K in DataVectors:
        AnalysisFilePtr.write('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n'%(K[0 ],K[1 ],K[2 ],K[3 ],K[4 ],K[5  ],K[6 ],K[7 ],K[8 ],K[9 ],K[10],K[11]))
    AnalysisFilePtr.close()
def VelvetIndividualAnalysis(FileName, VelvetAnalysisDir):
    """
    1)  Composite Velvet analysis takes all parameters (input and output params and puts them together
    2)  Individual Analysis makes a table of inputs as rows and outputs as columns
    """
    DataVectors = list()
    Path,FNAname = os.path.split(FileName) 
    SpeciesName = FNAname[0:-6]
    SpeciesLog = VelvetAnalysisDir+'/'+SpeciesName+'Analysis'

import locale
locale.setlocale(locale.LC_NUMERIC, "")
def format_num(num):
    """Format a number according to given places.
    Adds commas, etc. Will truncate floats into ints!"""

    try:
        inum = int(num)
        return locale.format("%.*f", (0, inum), True)

    except (ValueError, TypeError):
        return str(num)
def get_max_width(table, index):
    """Get the maximum width of the given column index"""
    return max([len(format_num(row[index])) for row in table])

def pprint_table(out, table):
    """Prints out a table of data, padded for alignment
    @param out: Output stream (file-like object)
    @param table: The table to print. A list of lists.
    Each row must have the same number of columns. """
    col_paddings = []

    for i in range(len(table[0])):
        col_paddings.append(get_max_width(table, i))

    for row in table:
        # left col
        print >> out, row[0].ljust(col_paddings[0] + 1),
        # rest of the cols
        for i in range(1, len(row)):
            col = format_num(row[i]).rjust(col_paddings[i] + 2)
            print >> out, col,
        print >> out
        
if __name__ == "__main__":
    VelvetAnalysis()