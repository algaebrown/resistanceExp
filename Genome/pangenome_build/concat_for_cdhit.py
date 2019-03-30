# list of all E.coli genomes in `genome`

def make_cdhit(list_path, output_file, gene_path):
    '''
    input:
    list_path = genome lists. for example(/home/hermuba/data0118/genome_list/ecoli_rm_plasmid_1582)
    output_file = concatenated, added genome ID to the end
    gene_path = folder containing .faa from prodigal. For example:'/home/hermuba/data/genePredicted/'

    output: None
    '''
    # open genome list file
    f = open(list_path)
    genome = f.readlines()
    for i in range(len(genome)):
        genome[i] = genome[i].rstrip().replace(u'\ufeff', '')

    #concat all .faa files into one single file
    from Bio import SeqIO
    outputHandle = open(output_file, 'a') # don't forget append mode or be stupid

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
