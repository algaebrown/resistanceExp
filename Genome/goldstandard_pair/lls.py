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
def lls(all_df):
    drop = ['gene_one', 'gene_two', 'goldstandard']
    score = list(set(all_df.columns) - set(drop))[0]

    all_df['cut_mutual'] = pd.qcut(all_df[score],  200)
    grouped = all_df.groupby(by = ['goldstandard', 'cut_mutual']).count()['gene_one']
    grouped = grouped.fillna(0)
    lls = grouped[1]/grouped[0]/(grouped[1].sum()/grouped[0].sum())
    #lls.plot()

    return(lls)


from scipy.stats import linregress
import numpy as np
# find the smallest LLS > 3, set as score threshold
def lls_regress_thres(lls):
    # drop inf and 0s
    lls = lls.replace([np.inf, -np.inf, 0], np.nan)
    lls.dropna(inplace = True)

    # find the smallest interval that is > 3
    thres = next(x[0] for x in enumerate(lls) if x[1] > 3)
    true_thres = lls.index[thres-1]

    # drop the LLS <3 and do regression
    lls_greater_three = lls[thres:]
    y = lls_greater_three.values
    x = np.array([interval.mid for interval in lls_greater_three.index])

    slope, intercept, r_value, p_value, std_err = linregress(x,y)


    return(true_thres, slope, intercept)

def map_lls(lls, true_thres, slope, intercept):
    x = np.array([interval.mid for interval in lls.index])
    y = slope * x + intercept

    new_lls = pd.Series(index = lls.index, data = y)
    new_lls[:true_thres] = 0
    return(new_lls)

def map_score_to_lls(all_df, new_lls):
    drop = ['gene_one', 'gene_two', 'goldstandard']
    score = list(set(all_df.columns) - set(drop))[0]

    all_df['lls'] = all_df[score].map(new_lls)

    return(all_df)

# PPV, NPV, coverage
def PPV_coverage(lls_thres, all_df):
    all_df['ans'] = all_df['lls'].map(lambda x: True if x > lls_thres else False)

    # calculate coverage
    total_nodes = set(all_df['gene_one']).union(set(all_df['gene_two']))
    net = all_df.loc[all_df['ans'] == True]
    covered_nodes = set(net['gene_one']).union(set(net['gene_two']))
    coverage = len(covered_nodes)/len(total_nodes)

    # calculate PPV
    grouped = all_df(by = ['goldstandard', 'ans']).count['gene_one']
    tp = grouped[1, True]
    fp = grouped[0, True]
    PPV = tp/(tp+fp)

    return(coverage, PPV)

def try_diff_lls_thres(all_df):
    # start from 3, 6, 12, 24, 48, 96, 132, 264, 528, 1056
    tradeoff = pd.DataFrame(columns = ['thres', 'coverage', 'PPV'])
    for t in [3,6,12,24,48,96,132,264,528, 1056]:
        cov, PPV = PPV_coverage(t, all_df)
        tradeoff.append([[t, cov, PPV]])
    return(tradeoff)


# map LLS_reg back to each "whole" network
