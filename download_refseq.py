# input file: assembly_result.txt from ASSEMBLY>TO FILE>ID TABLE

input_file = '/home/hermuba/data0118/refseq/ftpdirpaths'

# output directory:

out_dir = '/home/hermuba/data0118/refseq/gff'

# read file, to ID list

def to_id_list(input_file):

    '''
    this script is not useful at all
    instead use awk -F "\t" '$12=="Complete Genome" && $11=="latest"{print $20}' assembly_summary.txt > ftpdirpaths to generate complete path
    turn assembly.txt from ASSEMBLY to RefSeq id list
    input: path to assembly_result.txt
    output: a list containing all ids
    '''
    with open(input_file) as f:
        lines = f.readlines()

    # there are 4 columns: GenBank Assembly ID (Accession.version),GenBank release ID,RefSeq Assembly ID (Accession.version),RefSeq release ID
    # What we want is the 3rd one (index : 2)

    id_list = []

    for l in lines:
        ref_id = l.split('\t')[2]
        id_list.append(ref_id)

    return(id_list)

# download by rsync
import os
def download_ref_seq(input_file):

    with open(input_file) as f:
        paths = f.readlines()

    for p in paths:

        p = p[:-1] # remove \n

        # replace ftp with rsync, and we want only fna.gz only

        p = 'rsync'+ p[3:]  + '/' + p.split('/')[-1]+'_genomic.gff.gz'
        print(p)
        os.system('rsync --verbose ' + p + ' '+ out_dir)
