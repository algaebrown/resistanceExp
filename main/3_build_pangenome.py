import os
import pandas as pd
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-o", "--outdir", dest="outdir",
                  help="folder containing CD-HIT output")
parser.add_option("-g", "--genome_stat", dest="stat",
                  help="genome_stat.csv file")
parser.add_option("-p", "--prefix", dest="prefix",
                  help="prefix name")
parser.add_option("--prodigal", dest="prodigal_path",
                  help="none", default = 'prodigal_out')
(options, args) = parser.parse_args()



### INTERMEDIATE FILES ###
concat_faa_file = os.path.join(options.outdir, 'concat.faa')
### OUTPUTS ###
prefix = os.path.join(options.outdir,options.prefix) #faa for representing gene
clstr_file = prefix+'.clstr'
clstr_csv = prefix + '.clstr.csv'
repr_csv = prefix + '.repr.csv'

# find included genomes
genome_stat = pd.read_csv(options.stat, dtype = {'Unnamed: 0': str})
genome_stat.set_index('Unnamed: 0', inplace = True)
included_ids = genome_stat.loc[genome_stat['include']].index

######################### CD-HIT ################################
from Genome.pangenome_build.concat_for_cdhit import concat
if not os.path.isfile(concat_faa_file):
    print('Have not concat fasta files for CD-HIT yet. Concat now!')
    concat(included_ids, outfile=concat_faa_file, faa_path = options.prodigal_path)

# run CD-hit
if not os.path.isfile(prefix) or os.path.isfile(clstr_file):
    print('Found no CD-HIT output. Running CD-HIT')
    os.system('/home/hermuba/bin/cd-hit-v4.8.1-2019-0228/cd-hit -i {} -o {} -T 6 -c 0.7 -d 0 -M 10000'.format(concat_faa_file, prefix)) # output .clstr file and representing gene

print('CD-HIT outputs: {}, {}'.format(prefix, clstr_file))

# CD-hit .clstr file to 010101 (absence, presence csv; row = cluster; column = genome) and a representing gene mapper
from Genome.pangenome_intrinsic_info.cdhit_parse import clstr_to_csv, representing_gene_mapper
#clstr_to_csv(included_ids, clstr_file, clstr_csv)
representing_gene_mapper(clstr_file, repr_csv)

print('CD-HIT results parsed to: {} {}'.format(clstr_csv, repr_csv))


############################### Pan-genome statistics ########################################
os.system('python ~/resistanceExp/Genome/pangenome_intrinsic_info/count_core_acc.py {}'.format(clstr_file))
