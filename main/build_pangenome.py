glist = '/home/hermuba/data0118/genome_list/ecoli_rm_plasmid_1582'
concat_faa_file = '/home/hermuba/data0118/ec_remove_plasmid_1580.faa'
gene_path = '/home/hermuba/data/genePredicted/'

# concat for pangenome
from Genome.pangenome_build.concat_for_cdhit import make_cdhit
make_cdhit(glist, concat_faa_file, gene_path)

# run CD-hit
generic_fname = concat_faa_file.split('/')[-1].replace('.faa', '')

import os
os.system('bash ~/resistanceExp/Genome/pangenome_build/run_cdhit.sh' + ' ' + concat_faa_file + ' /home/hermuba/data0118/cdhit/' + generic_fname)

# parse to 0101010 file
d = '/home/hermuba/data0118/cdhit/clstr/pangenome_df/'
detail = '/home/hermuba/data0118/cdhit/clstr/cluster_detail/'
clstr_file = '/home/hermuba/data0118/cdhit/clstr/' + generic_fname + '.clstr'
from Genome.pangenome_intrinsic_info.cdhit_abs_only import clstr_abs
clstr_abs(glist, clstr_file, d)

# parse cluster detail file (containing header and member ID of each cluster)
from Genome.pangenome_intrinsic_info.parse_cdhit import clstr_detail
rep_gene_only(clstr_file, detail_path)

# run CARD: ERROR your shell has not been properly configured to use conda activate
# THIS STEP NEEDS TO BE DONE SEPERATEL
os.system('bash /home/hermuba/resistanceExp/Genome/run/card_for_rep_gene.sh ' + '/home/hermuba/data0118/cdhit/' + generic_fname + ' /home/hermuba/data0118/cdhit/card/' + generic_fname)

# run COG
os.system('/home/hermuba/data0118/cdhit/' + generic_fname + '> list')
os.system('perl /home/hermuba/bin/COGmapper/map_COG.pl list /home/hermuba/data0118/cdhit/cog/')

# run resfam
os.system('bash ~/resistanceExp/Genome/run/hmm_resfam.bash')

# run aclame
# run drug target
os.system('bash ~/resistanceExp/Genome/run/dmnd_aclame_drug.sh')
# run nr: 0.9.19 @ ywwwu/bin/diamond/diamond
os.system('bash ~/resistanceExp/Genome/run/dmnd_nr.sh')


# run interproscan
os.system('bash ~/resistanceExp/Genome/run/run_interproscan.sh')

# concat interproscan outputs
os.system('bash ~/resistanceExp/Genome/goldstandard_pair/concat_interpro.sh')

# extract pathway, goterm, ipraccession from interpro outputs
from Genome.goldstandard_pair.parse_interpro_out import parse, extract_term
interpro_file = '/home/hermuba/data0118/interpro/all'
df = parse(interpro_file)

go = extract_term(df, 'goterm')
path = extract_term(df, 'pathway')
ipr = extract_term(df, 'ipr_accession')

# parse card

# parse cog

# parse aclame, drug target, nr

# parse resfam

# run hypothetical protein, and generate pan-genome no. core/accessory

# read cluster_detail

# join all information
