from FastaSequence import *
import glob
def BorreliaBuilder(Directory):
    BorreliaCompositeFilename = Directory + "BorreliaComposite.fasta"
    BorreliaFiles = glob.glob(Directory +  "Borrelia*.fasta")
    Header = ">gi|ref|NC_000951| Borrelia burgdorferi B31 all plasmids"
    Sequences = list()
    for B in BorreliaFiles:
        K = fasta_read(B)
        Sequences.append(K[0])
    fasta_write(BorreliaCompositeFilename, Sequences,Header)

def SalmonellaBuilder(Directory):
    SalmonellaCompositeFilename = Directory + "SalmonellaComposite.fasta"
    SalmonellaFiles = glob.glob(Directory +  "Salmonella*.fasta")
    Header = ">gi|386730549|ref|NC_017718| Salmonella enterica subsp. enterica serovar Typhimurium str. SL1344 all plasmids "
    Sequences = list()
    for B in SalmonellaFiles:
        K = fasta_read(B)
        Sequences.append(K[0])
    fasta_write(SalmonellaCompositeFilename, Sequences,Header)
    
def fasta_write(output,seqs,header):
    """
        restricted fasta
        this format (used by biopropector) is just fasta with the whole sequence on one line.
        just write all sequences together
    """
    if type(output) == str: output=file(output,'w')
    output.write(header)
    for s in seqs:
        output.write("%s" % s.seq)
    output.close()

FastaDirectory = "/home/clinton/Projects/Pyllumina3/FastaFiles/"
BorreliaBuilder(FastaDirectory)
SalmonellaBuilder(FastaDirectory)