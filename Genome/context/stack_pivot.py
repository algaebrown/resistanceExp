# to stack pivot table for another way to discretise
rt_path = '/home/hermuba/data0118/discretize/'
fname = 'refseq_non_zero.csv'

#
import pandas as pd
def read_non_zero(fname):
    df = pd.read_csv(rt_path+fname, header = 0)

    s = pd.qcut(df['trans_evalue'], 98, labels = range(1,99), retbins =True)
    return(s)
