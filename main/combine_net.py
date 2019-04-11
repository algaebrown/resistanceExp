# combine four nets into one, yield combined_lls_edgelist
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def read_edge(net_name):
    path = '/home/hermuba/data0118/network1122/'
    filename = path + net_name + '_lls_edgelist'

    # skip first line header!!
    with open(filename, 'rb') as f:

        net = nx.read_edgelist(f, nodetype = str, comments = '#')
    return(net)

string = read_edge('string')
refseq = read_edge('refseq')
eskape = read_edge('eskape')
domain = read_edge('domain')
