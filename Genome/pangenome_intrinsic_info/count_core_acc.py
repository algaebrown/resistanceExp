import pandas as pd
import os
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys
mpl.style.use("seaborn-white")
def gene_distribution(pangenome_abs):
    '''
    return gene count v.s. gene prevalance hist
    '''
    df = pd.read_csv(pangenome_abs, index_col = 0, header = 0)
    count = df.sum(axis = 1) # Cluster 1 266...

    pan_size = df.shape[1]




    return count, pan_size, df

def extended_core(df):
    '''
    returns the def of extended core; threshold of count
    '''
    count = df.sum(axis = 1)
    n, bins, patches = plt.hist(count, bins = 100, color = 'grey')

    # maximal change
    dif = np.diff(n) # n = [1,3,9,18] dif = [2, 6, 9]; bins = [1,2,3,4,5]
    max_change = np.argmax(dif) # max_change = 2; essential index = 2 + 1 --> 18; anything > 4 is essential; bins [2+2]
    thres = bins[max_change + 1]

    return thres

def no_core(count, thres):
    return(len(count.loc[count >= thres]))


def pangenome_profile(df, bins = 100):
    ''' return # core/acc/pangenome per strain '''

    grow = pd.DataFrame(columns = ['core', 'accessory', 'pangenome'])

    no_of_sps = df.shape[1]


    for i in range(0,no_of_sps, math.ceil(no_of_sps/bins)): # cut number of genomes into 100 bins to save computational power

        count = df.iloc[:, :i+1] # index = sps; col = gene

        count = count.sum(axis = 1)

        all_genes = len(count.loc[count > 0])
        core_genes = len(count.loc[count >= i+1 * 0.989])
        acc = all_genes - core_genes

        grow.loc[i+1] = [core_genes, acc, all_genes]

    return grow

def pangenome_growth_curve(df, no_iter = 20, fig_path = 'fig'):
    ''' permute strain order, return mean and std of pan-genome growth curve 
    df: clstr_df'''
    results = []
    for n_iter in range(no_iter):
        genome_order = np.random.permutation(df.shape[1])
        permuted = df.iloc[:, genome_order]
        grow = pangenome_profile(permuted)
        results.append(grow.values) # append stats into np
    
    # calculate mean and std
    test = np.array(np.stack(results),dtype=np.float64) # weird bug

    grow_mean = np.mean(np.stack(results), axis = 0)
    grow_std = np.nanstd(test, axis = 0)


    # plotting
    fig, ax = plt.subplots()
    ax.set_xlabel('# Strain')
    ax.set_ylabel('# Gene Cluster')

    x = grow.index
    i = 0
    for label in grow.columns:
    
        ax.errorbar(x = x, y = grow_mean[:,i], yerr = grow_std[:,i], label = label)
        i+= 1
    plt.legend()
    plt.savefig(os.path.join(fig_path,'pangenome_growth.svg'), format = 'svg', dpi = 300)

    # save data
    pangenome_stats = pd.DataFrame(np.concatenate([grow_mean, grow_std], axis = 1), index = grow.index, columns = list(grow.columns)*2)
    return pangenome_stats

def gene_prevalance_plot(df, fig_path = '/nas2/users/hermuba/fig', bins = 100):
    ''' plot # gene versus prevalance, histogram '''
    count = df.sum(axis = 1)
    
    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(count, bins = bins, color = 'grey')
    ax.set_xlabel('gene prevalance')
    ax.set_xticks(range(0,df.shape[1],200))

    ax.set_ylabel('gene count')

    plt.savefig(os.path.join(fig_path, 'gene_prevalance.svg'), format = 'svg', dpi = 300)

if __name__=='__main__':
    clstr_csv = sys.argv[1]
    count, pan_size, clstr_df = gene_distribution(clstr_csv) # the path to pangenome clstr csv file

    # define core
    thres = extended_core(clstr_df) 

    # number
    n_core = no_core(count, thres)
    n_pan = len(count)
    n_acc = n_pan-n_core
    print('# Core {} Accessory {} Pangenome {}\n'.format(n_core, n_pan, n_acc))
    print('# Extended core thres {} ({:.0%})'.format(thres, thres/n_pan))

    # get growth curve
    pangenome_stats = pangenome_growth_curve(clstr_df)

    data_out = os.path.join(os.path.dirname(clstr_csv),'pangenome_grow_stat.csv')
    with open(data_out, 'w') as f:
        f.write('# Core {} Accessory {} Pangenome {} No.genome {}\n'.format(n_core, n_pan, n_acc, pan_size))
        f.write('# Extended core thres {} ({:.0%})'.format(thres, thres/pan_size))
    with open(data_out, 'a') as f:
    
        pangenome_stats.to_csv(f)
    print('data written to {}'.format(data_out))
    





    
    