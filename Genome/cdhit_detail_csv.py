import pandas as pd

def detail_csv(filename, outpath):
    # for output name
    f_name = filename.split('/')[-1]

    # tab delimited to be different for cluster members
    out_csv = open(outpath+f_name+'.tab', 'w')
    header = 'Cluster\trepresenting_gene\tmembers'
    out_csv.write(header + '\n')

    with open(filename) as f:

        new_line = ''
        member = ''

        for line in f:
            # a new cluster
            if line[0] == '>':

                # save the last cluster
                new_line = new_line + member # save the final results of all members
                if len(new_line) > 0:
                    out_csv.write(new_line + '\n')

                # a new cluster
                cluster_name = line.rstrip()[1:]
                new_line = cluster_name + '\t'

                member = ''
            else:
                # whether this gene is the representing gene
                is_represent = line[-2]

                # the gene's name and the genome it belongs to
                genome_id = line.split('|')[1].split('...')[0]
                gene_name = line.split('|')[0].split('>')[1]

                # concat member
                member = member + ',' + gene_name + '|' + genome_id


                if is_represent == '*':
                    new_line = new_line + gene_name + '|' + genome_id + '\t'
        # for the very last cluster
        new_line = new_line + member
        out_csv.write(new_line + '\n')
        out_csv.close()
        print("done with ", f_name)


from os import listdir
from os.path import isfile, join
mypath = '/home/hermuba/data0118/cdhit/clstr/'
onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]

outpath = mypath + 'cluster_detail/'

def wrapper(f):
    return(detail_csv(f,outpath))

from multiprocessing import Pool
with Pool(5) as p:
    print(p.map(wrapper, onlyfiles))
