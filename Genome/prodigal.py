import os

genome_path = "/home/hermuba/resistanceExp/genome"
gene_path = "home/hermuba/resistanceExp/genePredicted"
# to run prodigal
def run(ID):
    os.chdir(genome_path)
    print("running prodigal for " + ID) 
    os.system("prodigal -i "ID + ".fna -o garbage.gbk -a "+ ID+".faa")
    os.system("mv "+ID+".faa ../genePredicted/"+ID".faa")

# check if we already did it
def update(ID):
    onlyfiles = [f for f in os.listdir(gene_path) if os.path.isfile(os.path.join(gene_path, f))]
    if ID+'.faa' in onlyfiles:
        print("we already have prodical for ", ID)
    else run(ID)
