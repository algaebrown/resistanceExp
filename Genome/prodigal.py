import os

genome_path = "/home/hermuba/data/genome/"
gene_path = "/home/hermuba/data0118/predicted_genes/"
# to run prodigal

def run(ID):
    print("running prodigal for " + ID)
    os.system("prodigal -i "+ genome_path +'/'+ ID + ".fna -o garbage.gbk -a "+ ID+".faa -p meta")



# check if we already did it
def update(ID):
    os.chdir(gene_path)
    onlyfiles = [f for f in os.listdir('.') if os.path.isfile(os.path.join('./', f))]
    if ID+'.faa' in onlyfiles:
        print("we already have prodical for ", ID)
    else:
        run(ID)


with open("/home/hermuba/data/allgenomelist.txt", "r") as f:
    for ID in f.readlines():
        update(ID.replace('/n',''))
        #update(ID)
