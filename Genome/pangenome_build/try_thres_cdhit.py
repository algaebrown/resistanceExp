# try multiple threshold of cdhit
cdhit_path = "../../data0118/cdhit/"

import os
def run_cdhit(sps, threshold):

    os.system("cd-hit -i "+cdhit_path+sps+"_cdhit.faa -o "+cdhit_path+sps+threshold + " -d 0 -T 6 -M 120
000 -c "+ threshold)

# a list of all sps
list_path = "../../data0118/genomeList/"
all_list = os.listdir(list_path)

# remove all, drug list
all_list.remove('all')
all_list.remove('drug')

# a list of all threshold to try
thres = ['0.97', '0.95', '0.90', '0.80', '0.70']
for sps in all_list:
    for threshold in thres:
        run_cdhit(sps, threshold)

os.system("mv "+cdhit_path+'*.clstr '+cdhit_path+'clstr')
os.system("mv "+cdhit_path+'*.clstr '+cdhit_path+'clstr')
