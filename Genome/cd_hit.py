# preparing input file for cd-hit: append genome_ID into each gene

# list of all E.coli genomes in `genome`
genome_path = '../../data/genesPredicted'
genome_list_path =
output_path =
f = open(genome_list_path)
genome = f.readlines()
for i in range(len(genome)):
    genome[i] = genome[i].rstrip().replace(u'\ufeff', '')

from Bio import SeqIO
outputHandle = open(output_path, 'a') # don't forget append mode or be stupid

# read one files with SeqIO.parse() at a time
for ID in genome:
    recordIter = SeqIO.parse(genome_path + ID + '.faa', "fasta")

    # iterate through SeqRecords, annotate with ID
    for record in recordIter:
        # record.id = 'JAPM01000001_1'
        record.id = record.id + '|' + ID
        # record.id = JAPM01000001_1|1328440.3

        # output to one fasta file: `E.coli_cdhit.faa`
        SeqIO.write(record, outputHandle, "fasta")

outputHandle.close()
