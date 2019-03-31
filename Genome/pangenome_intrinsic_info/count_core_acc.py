import pandas as pd
def gene_distribution(pangenome_abs):
    '''
    return gene count v.s. gene prevalance hist
    '''
    df = pd.read_csv(pangenome_abs, index_col = 0, header = 0)
    count = df.sum(axis = 1) # Cluster 1 266...

    pan_size = df.shape[1]




    return(count, pan_size, df)

def extended_core(n, bins):
    '''
    returns the def of extended core; threshold of count
    '''
    import numpy as np
    dif = np.diff(n) # n = [1,3,9,18] dif = [2, 6, 9]; bins = [1,2,3,4,5]
    max_change = np.argmax(dif) # max_change = 2; essential index = 2 + 1 --> 18; anything > 4 is essential; bins [2+2]
    thres = bins[max_change + 1]

    return(thres)

def no_core(count, thres):
    return(len(count.loc[count >= thres]))

def pangenome_profile(df):

    grow = pd.DataFrame(columns = ['core', 'accessory', 'pangenome'])

    no_of_sps = df.shape[1]


    for i in range(no_of_sps):

        count = df.iloc[:, :i+1] # index = sps; col = gene

        count = count.sum(axis = 1)

        all_genes = len(count.loc[count > 0])
        core_genes = len(count.loc[count >= i+1 * 0.989])
        acc = all_genes - core_genes

        grow.loc[i+1] = [core_genes, acc, all_genes]

    return(grow)
