# softlink 300 genomes into 1 folder
# read PATRIC file
import pandas as pd
import os
import sys
genome_list=sys.argv[1]
df = pd.read_excel(genome_list, dtype = {'Genome ID':str}, engine='openpyxl')
id_list = df['Genome ID']

genome_path='/home/hermuba/nas2/prodigal_out'

print(id_list)
print(list(range(0,len(id_list), 300)))
batch_no=0
for n_genome in range(0,len(id_list), 300):
    print(batch_no)

    subdir=os.path.join(genome_path, f'batch{batch_no}')
    os.mkdir(subdir)

    print('symlink:', subdir)

    for genome in range(n_genome, n_genome +300):
        os.symlink(os.path.join(genome_path, id_list[genome]+'.faa'), os.path.join(subdir, id_list[genome]+'.faa'))
    
    batch_no += 1



#checkm lineage_wf -t 16 /home/hermuba/nas2/prodigal_out /home/hermuba/nas2/prodigal_out/checkm_out --genes -x faa --reduced_tree
#for folder in  /home/hermuba/nas2/prodigal_out/batch*; do checkm lineage_wf -t 16 $folder $folder --genes -x faa --reduced_tree; done
