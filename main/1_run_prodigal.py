# This script is to use prodigal to predict genes for all genomes
import os
import pandas as pd
import sys

genome_path = "/nas2/users/hermuba/genome/"
outdir = "/nas2/users/hermuba/prodigal_out/"
genome_list = sys.argv[1] # excel file downloaded in genome

# read PATRIC file
df = pd.read_excel(genome_list, dtype = {'Genome ID':str})
id_list = df['Genome ID']

# generate faa
for genome_id in id_list:
    if not os.path.isfile(os.path.join(outdir, '{}.faa'.format(genome_id))):
        os.system('prodigal -i {} -o tmp.gbk -a {}'.format(os.path.join(genome_path, '{}.fna'.format(genome_id)),
                                                            os.path.join(outdir, '{}.faa'.format(genome_id))
        ))
    else:
        print('already have {}'.format(genome_id))


#cd /home/hermuba/data/genome
#cat /home/hermuba/data0118/genomeList/all | parallel $HOME/bin/Prodigal/prodigal -i {}.fna -o t.gbk -a {}.faa
