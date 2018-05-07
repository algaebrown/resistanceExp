#
pfam_path = "/home/hermuba/data0118/cdhit/pfam/"

import pandas as pd
def parse(filename):
    """
    input:pfam_scan.pl output
    output:dataframe
    """
    # parse header
    h = '<seq id> <alignment start> <alignment end> <envelope start> <envelope end> <hmm acc> <hmm name> <type> <hmm start> <hmm end> <hmm length> <bit score> <E-value> <significance> <clan>'
    h = h[1:-1]
    h = h.split('> <')

    df = pd.read_csv(pfam_path + filename, comment = '#', delim_whitespace = True, names = h)
    df.to_pickle(pfam_path + 'df/' + filename)
    return(1)

import os

onlyfiles = [f for f in os.listdir(pfam_path) if os.path.isfile(os.path.join(pfam_path, f))]
for file in onlyfiles:
    parse(file)
