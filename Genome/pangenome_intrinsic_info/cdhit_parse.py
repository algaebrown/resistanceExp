import pandas as pd
def clstr_to_csv(genome_list,clstr_file,outfile):
    """
    clstr_to_df turns .clstr file generated from CD-HIT to dataframes. only absensce-presence pattern is returned to reduce memory usage. absence-presence pattern is stored in .csv format

    input:
    1. filename: .clstr file
    2. dfpath: the folder to store absence-presence dataframe

    the name of output dataframe will be FILENAME_df

    """
    # form the header of csv
    with open(outfile, 'w') as f:
        header = ','+','.join(genome_list) + '\n'
        f.write(header)

    
    # to parse .clstr
    out_csv = open(outfile, 'a')
    with open(clstr_file) as f:
        new_line = ''

        for line in f:

            if line[0] == '>': # new cluster
                if len(new_line) > 0: # save previous cluster
                    for val in clstr_dict.values():
                        new_line = new_line+val+','
                    out_csv.write(new_line[:-1]+'\n')


                # a new cluster
                clstr_name = line.rstrip()[1:]
                new_line = clstr_name + ',' # start a new line to store absence presence pattern
                clstr_dict = dict.fromkeys(genome_list, '0') # set all to 0


            else:
                genome_id = line.split('|')[1].split('...')[0]
                clstr_dict[genome_id] = '1'
    
    # after done looping the file, remember to save the last cluster
    for val in clstr_dict.values(): 
        new_line = new_line+val+','
    out_csv.write(new_line[-1]) # store from last cluster if "last cluster" exists

    out_csv.close()
    

def representing_gene_mapper(filename,outfile):
    ''' create Cluster 1 to faa mapper 
    filename: .clstr file
    outfile: output file'''
    
    print('write to '+ outfile)
    with open(filename) as f:
        for line in f:
            if line[0] == '>':
                clus = line.rstrip()[1:] # Cluster 1
            elif line[-2] == '*': # representing gene

                ID = line.split('|')[1].split('...')[0]
                gene_name = line.split('|')[0].split('>')[1]
                rep_name = gene_name + '|' + ID
                with open(outfile, 'a') as k:
                    k.write(','.join([clus,rep_name])+'\n')
if __name__=='__main__':

    #
    representing_gene_mapper(sys.argv[1], sys.argv[2])

    # genome list
    genome_stat = pd.read_csv(sys.argv[3], dtype = {'Unnamed: 0': str})
    genome_stat.set_index('Unnamed: 0', inplace = True)
    included_ids = genome_stat.loc[genome_stat['include']].index
    clstr_to_csv(included_ids, sys.argv[1], sys.argv[4])

