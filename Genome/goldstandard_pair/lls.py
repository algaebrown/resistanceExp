# a sampled GO-based goldstandard
import pandas as pd
def read_gold(gd):
    '''
    reads goldstandard file, returns dataframe
    input: gd = csv file containing goldstandard data, preferably sampled
    output: df, header = ['gene_one, 'gene_two', 'goldstandard']
    '''
    gold = pd.read_csv(gd, header = 0)
    gold = gold.rename(columns={"gene1": "gene_one", "gene2": "gene_two"}) # replace header; should be changed in generating tf_intersect

    return(gold)

# join network (one) into that sampled goldstandard
def read_net_by_chunk(net):
    '''
    read network file chunk by chunk, 100000 lines for a time
    input: file path
    '''
    all_chunks = pd.read_csv(net, header = 0, chunksize = 100000) # header not the same
    return(all_chunks)

def merge_net(gold, net_chunk):
    d1 = gold.merge(net_chunk, how = 'inner', left_on = ['gene_one', 'gene_two'], right_on = ['gene_one', 'gene_two'], sort = True)
    d2 = gold.merge(net_chunk, how = 'inner', left_on = ['gene_two', 'gene_one'], right_on = ['gene_one', 'gene_two'], sort = True) # in the future sort will not be needed due to change in pandas
    total = pd.concat([d1, d2])
    total = total.drop(['gene_one_x','gene_one_y', 'gene_two_x', 'gene_two_y'], axis = 1)

    return(total) # save only score and goldstandard

def merge_net_with_all_chunks(gold, all_chunks):
    '''
    returns merged goldstardard and score
    '''
    n = 0
    for chunk in all_chunks:
        total = merge_net(gold, chunk)
        if n == 0: # first chunk
            all_df = total
        else:
            all_df = pd.concat([all_df, total])
        n += 1
    return(all_df)


# discretize network score, infer LLS for each discretized network score
def lls_for_domain(all_df, score):
    '''
    lls calculator for domain-weighted net, using qcut, bin = 250 (optimized)
    input:
    all_df: joined dataframe with goldstandard and "score"
    score: the name of "score"; in this case: "weighted_mutual"

    '''
    #drop = ['gene_one', 'gene_two', 'goldstandard']
    #score = list(set(all_df.columns) - set(drop))[0] # context has two kinds of scores


    all_df['cut_mutual'] = pd.qcut(all_df[score],  250, duplicates = 'raise')



    grouped = all_df.groupby(by = ['goldstandard', 'cut_mutual']).count()['gene_one']
    grouped = grouped.fillna(0)
    lls_score = grouped[1]/grouped[0]/(grouped[1].sum()/grouped[0].sum())
    #lls.plot()

    return(lls_score)

def lls_for_other(all_df, score):
    """
    lls_for_other, lls calculator for other nets that cannot be discretized using qcut
    input:
    all_df: joined dataframe with goldstandard "score"
    score: for refseqNet and eskapeNet, either "nrm_mutual" or "mutual_info"; for STRING:
    """
    #drop = ['gene_one', 'gene_two', 'goldstandard']
    #score = list(set(all_df.columns) - set(drop))[0] # context has two kinds of scores


    all_df['cut_mutual'] = pd.cut(all_df[score],  300)



    grouped = all_df.groupby(by = ['goldstandard', 'cut_mutual']).count()['gene_one']
    grouped = grouped.fillna(0)
    lls_score = grouped[1]/grouped[0]/(grouped[1].sum()/grouped[0].sum())
    #lls.plot()

    return(lls_score)


from scipy.stats import linregress
import numpy as np
# find the smallest LLS > 3, set as score threshold
def lls_regress_thres(lls_score):
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
    thres = next(x[0] for x in enumerate(lls_score) if x[1] > 3)
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
def PPV_coverage(lls_thres, all_df):
    '''
    calculate PPV, coverage using different threshold of LLS cutoff
    input: lls_thres: the LLS cutoff to consider interaction as True
    all_df: dataframe containing goldstandard and lls
    '''
    all_df['ans'] = all_df['lls'].map(lambda x: True if x > lls_thres else False)

    # calculate coverage
    total_nodes = set(all_df['gene_one']).union(set(all_df['gene_two']))
    net = all_df.loc[all_df['ans'] == True]
    covered_nodes = set(net['gene_one']).union(set(net['gene_two']))
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
def try_diff_lls_thres(all_df):
    '''
    try different LLS threshold to see the tradeoffs between coverage and PPV
    LLS threshold as df['lls'].unique values
    all_df: dataframe containing goldstandard and lls
    '''
    tradeoff = pd.DataFrame(columns = ['thres', 'coverage', 'PPV'])

    try_list = np.sort(all_df['lls'].unique())[1:-1]
    for t in try_list:
        cov, PPV = PPV_coverage(t, all_df)
        tradeoff.loc[t] = [t, cov, PPV]
    return(tradeoff)

# map LLS_reg back to each "whole" network

def map_lls_to_whole_data(net, new_lls, score, true_thres, output_file, net_name):
    '''
    map LLS to whole data and save to file
    drop LLS < 3: their LLS will be zero so no information :(
    '''

    from networkx.convert_matrix import from_pandas_edgelist
    from networkx import write_edgelist

    n = 0

    # initiate file
    with open(output_file, 'w') as f:
        f.write('#generating from '+net + '\n')

    all_chunks = read_net_by_chunk(net)
    for chunk in all_chunks:

        # drop LLS < 3 by excluding thres:
        dropped = chunk.loc[chunk[score] > true_thres.right]

        # map new_lls to df score
        mapped = map_score_to_lls(dropped, new_lls, score)
        print(mapped.shape)

        mapped.fillna(value = 2*new_lls[-1]-new_lls[-2], inplace = True) # the right bound lls may not be captured by new_lls due to sampling
        print(2*new_lls[-1]-new_lls[-2]) # the right bound lls may not be captured by new_lls due to sampling

        mapped = mapped.loc[mapped['lls'] >= 3]
        print(mapped.shape)

        mapped.rename(axis = 'columns', mapper = {'lls': net_name + '_lls'}, inplace = True)

        # convert to edgelist
        G = from_pandas_edgelist(mapped, source = 'gene_one', target = 'gene_two', edge_attr = net_name + '_lls')

        # write to file
        with open(output_file, 'ab') as f:
            write_edgelist(G, f, data = True)


            n += 1
    print('done with '+net_name)
