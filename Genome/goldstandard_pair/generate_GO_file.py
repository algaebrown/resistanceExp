# input = dataframe with all the annotations
# output = tf_intersect file


# input file
infile = '/home/hermuba/data0118/goldstandard/ec_rmplasmid_node_anno_df'

from Genome.goldstandard_pair.make_gold_file import gold_standard
import pandas as pd

# read annotation dataframe
df = pd.read_pickle(infile)

# extract go terms
GO_file = '/home/hermuba/data0118/goldstandard/tf_intersect_GO_rm_plasmid'
no_redun_go = gold_standard(df, 'GO', GO_file)

# extract pathway terms
path_file = '/home/hermuba/data0118/goldstandard/tf_intersect_pathway_rm_plasmid'
no_redun_path = gold_standard(df, 'pathway', path_file)
