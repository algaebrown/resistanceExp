# a sampled GO-based goldstandard
import pandas as pd
from math import floor
gold_anno = pd.read_pickle('/home/hermuba/data0118/goldstandard/ec_rmplasmid_node_anno_df')
def read_gold(gd, colnames = None):
    '''
    reads goldstandard file, returns dataframe
    input: gd = csv file containing goldstandard data, preferably sampled
    output: df, header = ['gene_one, 'gene_two', 'goldstandard']
    '''
    if colnames:
        gold = pd.read_csv(gd, header = None, names = colnames)
    else:
        gold = pd.read_csv(gd, header = 0)
   

    return(gold)

# join network (one) into that sampled goldstandard
def read_net_by_chunk(net, chunksize = 100000, names = None):
    '''
    read network file chunk by chunk, 100000 lines for a time
    input: file path
    '''
    if names:
        all_chunks = pd.read_csv(net, names = names, chunksize = chunksize) # header not the same
    else:
        all_chunks = pd.read_csv(net, header = 0, chunksize = chunksize) # header not the same
    return(all_chunks)

def merge_net(gold, net_chunk, net_name = 'eskape'):
    d1 = gold.merge(net_chunk, how = 'inner', left_on = ['gene_one', 'gene_two'], right_on = ['gene_one', 'gene_two'], sort = True, suffixes = (None, '_' + net_name))
    d2 = gold.merge(net_chunk, how = 'inner', left_on = ['gene_two', 'gene_one'], right_on = ['gene_one', 'gene_two'], sort = True, suffixes = (None, '_' + net_name)) # in the future sort will not be needed due to change in pandas
    total = pd.concat([d1, d2])
    
    total.drop(columns = ['gene_one_{}'.format(net_name),'gene_two_{}'.format(net_name)], inplace = True)
    
    return(total) # save only score and goldstandard

def merge_net_with_all_chunks(gold, all_chunks, net_name):
    '''
    returns merged goldstardard and score
    '''
    n = 0
    for chunk in all_chunks:
        total = merge_net(gold, chunk, net_name = net_name)
        if n == 0: # first chunk
            all_df = total
        else:
            if n%100 == 0:
                print('processing {} chunk'.format(n))
            all_df = pd.concat([all_df, total], axis = 0, sort = False)
        n += 1
    return(all_df)


#################################### DISCRETIZE AND FIT LLS #################################################
# discretize network score, infer LLS for each discretized network score
def lls_for_domain(all_df, score, bins = 250):
    '''
    lls calculator for domain-weighted net, using qcut, bin = 250 (optimized)
    input:
    all_df: joined dataframe with goldstandard and "score"
    score: the name of "score"; in this case: "weighted_mutual"

    '''
    #drop = ['gene_one', 'gene_two', 'goldstandard']
    #score = list(set(all_df.columns) - set(drop))[0] # context has two kinds of scores


    all_df['cut_mutual'] = pd.qcut(all_df[score],  bins, duplicates = 'drop')



    grouped = all_df.groupby(by = ['goldstandard', 'cut_mutual']).count()['gene_one']
    grouped = grouped.fillna(0)
    
     # pseudocount
    L_E = grouped[1] + 1
    not_L_E = grouped[0] + 1
    L = grouped[1].sum()+1
    not_L = grouped[0].sum()+1
    
    
    lls_score = (L_E/not_L_E)/(L/not_L)


    return np.log(lls_score)

def lls_for_other(all_df, score, bins = 300):
    """
    lls_for_other, lls calculator for other nets that cannot be discretized using qcut
    USING PSEUDOCOUNT
    input:
    all_df: joined dataframe with goldstandard "score"
    score: for refseqNet and eskapeNet, either "nrm_mutual" or "mutual_info"; for STRING:
    """
    #drop = ['gene_one', 'gene_two', 'goldstandard']
    #score = list(set(all_df.columns) - set(drop))[0] # context has two kinds of scores

    #
    all_df['cut_mutual'] = pd.cut(all_df[score],  bins)


    # count in each bin how many positive example and how many negative example
    grouped = all_df.groupby(by = ['goldstandard', 'cut_mutual']).count()['gene_one'].fillna(0)
    
    # pseudocount
    L_E = grouped[1] + 1
    not_L_E = grouped[0] + 1
    L = grouped[1].sum()+1
    not_L = grouped[0].sum()+1
    
    
    lls_score = (L_E/not_L_E)/(L/not_L)
    #lls.plot()

    return np.log(lls_score)


from scipy.stats import linregress
import numpy as np
# find the smallest LLS > 3, set as score threshold
def lls_regress_thres(lls_score, lls_thres = 3):
    """
    perform linear regression to assign LLS to interactions without benchmarking data
    input: lls_score

    procedure: drop np.inf, -np.inf and LLS = 0
    keep only LLS > 3 as the theshold of inclusion
    regress on the remaining

    output:
    - true_thres: score threshold where LLS > 3; below this threshold LLS will be assigned to 0
    - slope
    - intercept
    """
    # drop inf and 0s
    lls_score = lls_score.replace([np.inf, -np.inf, 0], np.nan)
    lls_score.dropna(inplace = True)

    # find the smallest interval that is > 3
    thres = next(x[0] for x in enumerate(lls_score) if x[1] > lls_thres)
    true_thres = lls_score.index[thres-1]

    # drop the LLS<3 and do regression
    lls_greater_three = lls_score[thres:]
    y = lls_greater_three.values
    x = np.array([interval.mid for interval in lls_greater_three.index])

    slope, intercept, r_value, p_value, std_err = linregress(x,y)


    return(true_thres, slope, intercept)

def map_lls(lls_score, true_thres, slope, intercept):
    '''
    making a lls mapper based on the regression and threshold
    '''
    x = np.array([interval.mid for interval in lls_score.index])
    y = slope * x + intercept

    new_lls = pd.Series(index = lls_score.index, data = y)
    new_lls[:true_thres] = 0

    # add infintie to the right side

    return(new_lls)

def map_score_to_lls(all_df, new_lls, score):
    '''
    mapping the lls score (regressed) to a dataframe containing "score"
    - all_df: dataframe containing score
    - new_lls: score -> lls mapper series
    - score: specify the score name "weighted_mutual", "nrm_mutual", "mutual"
    '''
    #drop = ['gene_one', 'gene_two', 'goldstandard']
    #score = list(set(all_df.columns) - set(drop))[0]

    all_df['lls'] = all_df[score].map(new_lls)

    return(all_df)

# PPV, NPV, coverage
def PPV_coverage(lls_thres, all_df, gold, score_colname = 'lls', gene_set = 'all', gold_anno = gold_anno):
    '''
    calculate PPV, coverage using different threshold of LLS cutoff
    input: lls_thres: the LLS cutoff to consider interaction as True
    all_df: dataframe containing goldstandard and lls
    gold: goldstandard file
    gene_set: 'all', 'core', 'accessory'
    '''
    all_df['ans'] = all_df[score_colname].map(lambda x: True if x > lls_thres else False)

    # calculate coverage

    # prepare gold standard
    total_nodes = set(gold['gene_one']).union(set(gold['gene_two']))
    if gene_set == 'all':
        pass
    if gene_set == 'core':
        genes = gold_anno.loc[gold_anno['core']].index.tolist()
        total_nodes = total_nodes.intersection(set(genes))
        #print('total goldstandard in core:{}'.format(len(total_nodes)))

    if gene_set == 'accessory':
        genes = gold_anno.loc[~gold_anno['core']].index.tolist()
        total_nodes = total_nodes.intersection(set(genes))
        #print('total goldstandard in accessory:{}'.format(len(total_nodes)))



    # get the network
    net = all_df.loc[all_df['ans'] == True]
    covered_nodes = set(net['gene_one']).union(set(net['gene_two']))
    if gene_set == 'core':
        genes = gold_anno.loc[gold_anno['core']].index.tolist()
        covered_nodes = covered_nodes.intersection(set(genes))
        #print('covered core in Net:{}'.format(len(covered_nodes)))

    if gene_set == 'accessory':
        genes = gold_anno.loc[~gold_anno['core']].index.tolist()
        covered_nodes = covered_nodes.intersection(set(genes))
        #print('covered accessory in net:{}'.format(len(covered_nodes)))

    coverage = len(covered_nodes)/len(total_nodes)

    # calculate PPV
    grouped = all_df.groupby(by = ['goldstandard', 'ans']).count()['gene_one']

    try:
        tp = grouped[1, True]
        fp = grouped[0, True]
        PPV = tp/(tp+fp)
    except KeyError:
        PPV = 0

    return(coverage, PPV)
def try_diff_lls_thres(all_df, gold, score_colname = 'lls', gene_set = 'all'):
    '''
    try different LLS threshold to see the tradeoffs between coverage and PPV
    LLS threshold as df['lls'].unique values
    all_df: dataframe containing goldstandard and lls
    '''
    tradeoff = pd.DataFrame(columns = ['thres', 'coverage', 'PPV'])

    # join back the gold to get a more genuine coverage
    
    possible_score = np.sort(all_df[score_colname].unique())

    # emphasize on high scores
    high_score_bins = possible_score[-50:]
    
    step = floor(len(possible_score)/50)
    if step == 0:
        step = 1
    spacing_index = np.arange(0, len(possible_score), step = step)
    try_list = list(possible_score[spacing_index]) + list(high_score_bins)
    
    
    for t in try_list:
        cov, PPV = PPV_coverage(t, all_df, gold, score_colname = score_colname, gene_set = gene_set)
        tradeoff.loc[t] = [t, cov, PPV]
    return(tradeoff)

# map LLS_reg back to each "whole" network

def map_lls_to_whole_data(net, new_lls, score, output_file, net_name, lls_thres = 3):
    '''
    map LLS to whole data and save to file
    drop LLS < 3: their LLS will be zero so no information :(
    '''

    from networkx.convert_matrix import from_pandas_edgelist
    from networkx import write_edgelist

    n = 0
    total_edge = 0
    # initiate file
    with open(output_file, 'w') as f:
        f.write('#generating from '+net + '\n')

    all_chunks = read_net_by_chunk(net)
    for chunk in all_chunks:

        dropped = chunk.loc[chunk[score]>new_lls.index[0].left] # only pick those have in the interval
        # map new_lls to df score
        mapped = map_score_to_lls(dropped, new_lls, score)
        
        mapped.fillna(value = new_lls.max(), inplace = True) # the right bound lls is fitted by the best value
    
        mapped = mapped.loc[mapped['lls'] >= lls_thres]
        
        total_edge += mapped.shape[0]
        if n% 100 == 0:
            print('at {} chunk, we have {} edges with lls > {}'.format(n,total_edge, lls_thres))

        mapped.rename(axis = 'columns', mapper = {'lls': net_name + '_lls'}, inplace = True)

        # convert to edgelist
        G = from_pandas_edgelist(mapped, source = 'gene_one', target = 'gene_two', edge_attr = net_name + '_lls')

        # write to file
        with open(output_file, 'ab') as f:
            write_edgelist(G, f, data = True)


            n += 1
    print('done with '+net_name)
