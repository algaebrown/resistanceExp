# directories
gene_path = "../../data0118/predicted_genes/"
cdhit_path = "../../data0118/cdhit/"
list_path = "../../data0118/genomeList/"

# list of all E.coli genomes in `genome`

def make_cdhit(species):
    # open genome list file
    f = open(list_path + species)
    genome = f.readlines()
    for i in range(len(genome)):
        genome[i] = genome[i].rstrip().replace(u'\ufeff', '')

    #concat all .faa files into one single file
    from Bio import SeqIO
    outputHandle = open(cdhit_path + species + '_cdhit.faa', 'a') # don't forget append mode or be stupid

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

# run for all species

import os
all_list = os.listdir(list_path)

# remove all, drug list
all_list.remove('all')
all_list.remove('drug')

for sps in all_list:
    make_cdhit(sps)
