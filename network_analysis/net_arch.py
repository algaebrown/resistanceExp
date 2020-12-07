# to analyze a single network

import pandas as pd
import numpy as np
import networkx as nx
from scipy import stats

def read_csv_to_network(infile):

    with open(infile, 'rb') as f:
        # skip header
        next(f)


        # read to net
        net = nx.read_edgelist(path = f,
                               delimiter = ',',
                               nodetype = str,
                               data = (('weighted_mutual', float),))
        # other types of network might need more data items
        return(net)

def network_stats(net):
    print('number of nodes, number of edges, number of subclusters')
    return(nx.number_of_nodes(net), nx.number_of_edges(net), nx.algorithms.components.number_connected_components(net))

def power_law(net):
    '''
    input: networkx net
    output: logx, logy, line, slope, r_value, p_value
    '''
    deg_seq = np.asarray(list(dict(net.degree()).values()))
    hist, bins = np.histogram(deg_seq, bins = 50)
    print('most connected node degree ', np.max(deg_seq))

    # remove 0
    new_hist = hist[hist != 0]
    bins = bins[:-1]
    bins = bins[hist != 0]

    # covert to log to plot and regression
    logx = np.log10(bins)
    logy = np.log10(new_hist)

    # regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(logx, logy)
    line = slope * logx+ intercept


    return(logx, logy, line, slope, r_value, p_value)
