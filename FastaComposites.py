from FastaSequence import *
import glob
def BorreliaBuilder(Directory):
    BorreliaCompositeFilename = Directory + "BorreliaComposite.fasta"
    BorreliaFiles = glob.glob(Directory +  "Borrelia*.fasta")
    Sequences = list()
    for B in BorreliaFiles:
        Sequences.append(fasta_read(B))
    fasta_write(BorreliaCompositeFilename, Sequences)
    
def fasta_write(output,seqs):
    """
        restricted fasta
        this format (used by biopropector) is just fasta with the whole sequence on one line.
        just write all sequences together
    """
    if type(output) == str: output=file(output,'w')
    for s in seqs:
        output.write("> %s\n" % s.header)
        output.write("%s\n" % s.seq)
        
        REBUILD LINUX KERNEL