# directories
gene_path = "../../data/genePredicted/"
cog_path = "../../data/genePredicted/cdhit/"
list_path = "../../data/ECgenome.txt"

# list of all E.coli genomes in `genome`

f = open(list_path)
genome = f.readlines()
for i in range(len(genome)):
    genome[i] = genome[i].rstrip().replace(u'\ufeff', '')

from Bio import SeqIO
outputHandle = open(cog_path + 'cdhit.faa', 'a') # don't forget append mode or be stupid

# read one files with SeqIO.parse() at a time
for ID in genome:
    recordIter = SeqIO.parse(gene_path + ID + '.faa', "fasta")

    # iterate through SeqRecords, annotate with ID
    for record in recordIter:
        # record.id = 'JAPM01000001_1'
        record.id = record.id + '|' + ID
        # record.id = JAPM01000001_1|1328440.3

        # output to one fasta file: `E.coli_cdhit.faa`
        SeqIO.write(record, outputHandle, "fasta")

outputHandle.close()
