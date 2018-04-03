# a script to run CARD(comprehensive antibiotic resistance database) annotation

# path
gene_path = "/home/hermuba/resistanceExp/genePredicted"
txt_path = "/home/hermuba/resistanceExp/genePredicted/resGeneTxt"
json_path = "/home/hermuba/resistanceExp/genePredicted/resGeneJson"
# import
from package import rgi
import os, errno
# to run card
def run(ID):
    print("running CARD annotation for "+ID)
    os.chdir(gene_path)
    os.system("rgi -t 'protein' -i "+ ID +".faa -o " + ID)
    os.system("mv "+ ID+".txt "+ txt_path)
    os.system("mv "+ ID+".json "+ json_path)

# update
def update(ID):
    onlyfiles = [f for f in os.listdir(txt_path) if os.path.isfile(os.path.join(txt_path, f))]
    if ID+'.txt' in onlyfiles:
        print("we already have CARD for ", ID)
    else:
        run(ID)

# run card for all *.faa in a folder

def folder_card(folder):
    onlyfiles = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    try:
        os.makedirs(folder + 'card')
        print("folder `card` mades under " + folder + ' to contain output')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    for f in onlyfiles:
        os.system("rgi -t 'protein' -i "+ folder + f  +" -o " + folder + 'card/'+f)
