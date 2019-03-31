import pandas as pd


def clstr_detail(filename,detailpath):
    """
    Turn .clstr to cluster-detail.csv; header = representing_gene, members; index = CLuster 1

    input:
    1. filename: .clstr file

    3. detail path: the folder to store cluster_detail dataframe
    the name of output dataframe will be FILENAME_df and FILENAME_cluster_detail

    """


    # create dataframe


    cluster_detail = pd.DataFrame(columns = ['representing_gene'])

    with open(filename) as f:
        for line in f:

            if line[0] == '>':

                columnName = line.rstrip()[1:]
                print(columnName)


                member = ''
            else:

                isrepresent = line[-2]
                ID = line.split('|')[1].split('...')[0]
                number = int(line.split('\t')[0])+1


                gene_name = line.split('|')[0].split('>')[1]



                # save member
                member = member + ',' + gene_name + '|' + ID
                cluster_detail.loc[columnName, 'members'] = member

                if isrepresent == '*':
                    cluster_detail.loc[columnName, 'representing_gene'] = gene_name + '|' + ID

















    cluster_detail.to_csv(detailpath+f_name+'.csv')

    return(cluster_detail)

def rep_gene_only(filename,detailpath):
    f_name = filename.split('/')[-1]
    print('write to '+ detailpath + f_name)
    with open(filename) as f:
        for line in f:
            if line[0] == '>':
                clus = line.rstrip()[1:] # Cluster 1
            elif line[-2] == '*': # representing gene

                ID = line.split('|')[1].split('...')[0]
                gene_name = line.split('|')[0].split('>')[1]
                rep_name = gene_name + '|' + ID
                with open(detailpath+f_name, 'a') as k:
                    k.write(','.join([clus,rep_name])+'\n')
