from Bio import SeqIO
import os
from optparse import OptionParser


parser = OptionParser()
parser.add_option("-o", "--outdir", dest="out",
                  help="concat.faa")

(options, args) = parser.parse_args()
def concat(faa_files, outfile):
    '''
    concatenate all gene's faa into a single faa for cdhit
    input
    genome_ids: list containing genome ids
    faa_path: folder to all fasta files
    outfile: concatenated file
    '''
    
    # read one files with SeqIO.parse() at a time
    for i, faa_file in enumerate(faa_files):
        print('onefaa', faa_file)
        ID = os.path.splitext(os.path.basename(faa_file))[0]
        print(ID)
        recordIter = SeqIO.parse(faa_file, "fasta")

        if i == 0:
            if not os.path.isdir(os.path.dirname(outfile)): 
                os.mkdir(os.path.dirname(outfile))
            f = open(outfile, 'w')
        else:
            f = open(outfile, 'a')
        

        # iterate through SeqRecords, annotate with ID
        for record in recordIter:
            # record.id = 'JAPM01000001_1'
            record.id = record.id + '|' + ID
            # record.id = JAPM01000001_1|1328440.3

            # output to one fasta file: `E.coli_cdhit.faa`
            SeqIO.write(record, f, "fasta")

        f.close()

if __name__=="__main__":
    
    print('args', args)
    concat(args, options.out)