def clstr_abs(filename,dfpath):
    """
    clstr_to_df turns .clstr file generated from CD-HIT to dataframes. only absensce-presence pattern is returned to reduce memory usage. absence-presence pattern is stored in .csv format

    input:
    1. filename: .clstr file
    2. dfpath: the folder to store absence-presence dataframe

    the name of output dataframe will be FILENAME_df

    """
    # obtain species list:
    sps_name = filename.split('/')[-1].split('0')[0]
    genome_list_path = "/home/hermuba/data0118/genomeList/"
    header = ','

    genome_list = []
    with open(genome_list_path + sps_name) as sps_list:
        for line in sps_list:
            header = header+line.replace('\n', '')+','
            genome_list.append(line.replace('\n', ''))

        #print(header)
    # open output pipe
    f_name = filename.split('/')[-1]
    out_csv = open(dfpath+f_name+'.csv', 'w')
    out_csv.write(header[:-1]+'\n') # remove the last ','

    # to parse .clstr
    with open(filename) as f:
        new_line = ''

        for line in f:

            if line[0] == '>':
                if len(new_line) > 0:
                    for val in clstr_dict.values():

                        new_line = new_line+val+','

                    out_csv.write(new_line[:-1]+'\n') # store from last cluster if "last cluster" exists


                # a new cluster
                clstr_name = line.rstrip()[1:]

                new_line = clstr_name + ',' # start a new line to store absence presence pattern
                clstr_dict = dict.fromkeys(genome_list, '0') # set all to 0


            else:


                genome_id = line.split('|')[1].split('...')[0]
                clstr_dict[genome_id] = '1'

    for val in clstr_dict.values(): # for the last cluster

        new_line = new_line+val+','
    out_csv.write(new_line[-1]) # store from last cluster if "last cluster" exists

    out_csv.close()
    print("done with ", f_name)

# run for all files
from os import listdir
from os.path import isfile, join
mypath = '/home/hermuba/data0118/cdhit/clstr/'
onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]

# wrapper
outpath = mypath + 'pangenome_df/'
def wrap_clstr(f):
    return(clstr_abs(f, outpath))

from multiprocessing import Pool
with Pool(5) as p:
    print(p.map(wrap_clstr, onlyfiles))
