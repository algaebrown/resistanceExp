# read gene list
with open("/home/hermuba/data/genomeList/ECgenome.txt") as f:
    genome_list = f.readlines()
for i in range(len(genome_list)):
    genome_list[i] = genome_list[i].replace('\n', '')

# run prokka to prepare roary output
import os
prokka_path = '/home/hermuba/bin/prokka/bin/'
path = '/home/hermuba/data/genome/'
for genome in genome_list:
    os.chdir(path + 'prokka')
    os.system(prokka_path + "prokka --kingdom Bacteria --outdir "+ path + "prokka/" + genome + " --locustag +" + genome + ' ' +  path + genome + ".fna")

# run roary
os.system("roary -f " + path + 'prokka/' + " -e -n -v " + path+ 'prokka/' + "*.gff")
