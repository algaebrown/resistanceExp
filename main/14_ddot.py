################## BUILD ONTOLOGY #####################
# DRUG SPECIFIC
mero_subnet = pd.read_excel(net_path, sheet_name = 'meropenem')['source', 'target', 'total_score']
ont2 = Ontology.run_clixo(mero_subnet,  alpha = 0.05 , beta = 0.5,square=False, output = '/home/hermuba/nas2/integrate_net/mero.whole.clixo')

# PAN-RESISTOME
panresist_gene = gold_anno.loc[~gold_anno['core']].index
panresist_subnet = data.loc[(data['source'].isin(panresist_gene)) & (data['target'].isin(panresist_gene)), ['source', 'target', 'total_score']]
pan_ont=Ontology.run_clixo(panresist_subnet,  alpha = 0.05 , beta = 0.5,square=False, output = '/home/hermuba/nas2/integrate_net/pan.whole.clixo')

############### UPDATE NODE ATTRIBUTE ###################
ont2.update_node_attr(gold_anno_str)
pan_ont.update_node_attr(gold_anno_str)


############## ALIGN TO GENE ONTOLOGY ##########################
# PARSE GENE ONTOLOGY FILES
onto_root = '/home/hermuba/data0118/ontologies/'
from ddot.Ontology import parse_obo
parse_obo(onto_root+'go-basic.obo', output_file = onto_root+'go.ddot', id2name_file = onto_root+'go_id2name.ddot', id2namespace_file = onto_root+'go_id2namespace.ddot')

# CREATE GENE TERM MAPPING FOR EACH ONTOLOGY
def get_gene_term_table(ont, gold_anno = gold_anno):
    geneterm = []
    gt = gold_anno.loc[[int(i) for i in ont.genes], 'GO']
    for g in gt.index:
        if type(gt[g]) == set:
            for goterm in list(gt[g]):
                geneterm.append([goterm, g])
    geneterm = pd.DataFrame(geneterm, columns = ['go_term', 'gene'])
    
    return geneterm
ont2_geneterm = get_gene_term_table(ont2)
pan_ont_geneterm = get_gene_term_table(pan_ont)

# BUILD DDOT ONTOLOGY OBJECT
go_ont2 = Ontology.from_table(onto_root+'go.ddot', mapping = ont2_geneterm, mapping_parent = 'go_term', mapping_child = 'gene', propagate = None)
go_panont = Ontology.from_table(onto_root+'go.ddot', mapping = pan_ont_geneterm, mapping_parent = 'go_term', mapping_child = 'gene', propagate = None)

# ALINGMENT
align_ont2 = ont2.align(go_ont2)
align_pan_ont = pan_ont.align(go_panont)

# ANNOTATE GO TERM
go_name = pd.read_csv('/home/hermuba/data0118/ontologies/go_id2name.ddot', sep = '\t', names = ['Name'], index_col = 0)
align_pan_ont['name'] = align_pan_ont['Term'].map(go_name['Name'])
align_ont2['name'] = align_ont2['Term'].map(go_name['Name'])

#################### ALIGN TO ARO ############################
import sys
sys.path.append('~/resistanceExp/visualization/exp12_Ontology/')
from obo_aro import parse_obo
parse_obo('/home/hermuba/data0118/ontologies/aro.obo', '/home/hermuba/data0118/ontologies/aro_output')

# create gene term table
def get_gene_term_table_ARO(ont, gold_anno = gold_anno):
    geneterm = []
    gt = gold_anno.loc[[int(i) for i in ont.genes], 'ARO'].to_frame().reset_index()
    gt.dropna(subset = ['ARO'], inplace = True)
    gt['ARO'] = 'ARO:'+gt['ARO'].astype(int).astype(str)
    
    return gt

ont2_geneterm_aro = get_gene_term_table_ARO(ont2)
pan_ont_geneterm_aro = get_gene_term_table_ARO(pan_ont)

aro_ontology_ont2 = Ontology.from_table('/home/hermuba/data0118/ontologies/aro_output', mapping = ont2_geneterm_aro, mapping_parent = 'ARO', mapping_child = 'gene_id')
aro_ontology_pan = Ontology.from_table('/home/hermuba/data0118/ontologies/aro_output', mapping = pan_ont_geneterm_aro, mapping_parent = 'ARO', mapping_child = 'gene_id')

# alignment
align_ont2_aro = ont2.align(aro_ontology_ont2)
align_pan_ont_aro = pan_ont.align(aro_ontology_pan)

aro_name = pd.read_csv('~/data0118/ontologies/aro.tsv', header = 0, sep = '\t', index_col = 0)
aro_name = aro_name.loc[~aro_name.index.duplicated()]
align_ont2_aro['name'] = align_ont2_aro['Term'].map(aro_name['Name'])
align_pan_ont_aro['name'] = align_pan_ont_aro['Term'].map(aro_name['Name'])

################## COMPARE TWO ALIGNMENTS ##########################
for ont in [align_ont2_aro, align_ont2, align_pan_ont, align_pan_ont_aro]:
    ont['Term index'] = ont.index

merged_ont2 = align_ont2_aro.merge(align_ont2, left_on = 'Term index', right_on = 'Term index', how = 'outer').merge(aro_name, left_on = 'Term_x', right_on = 'Accession', how = 'left')
merged_pan = align_pan_ont_aro.merge(align_pan_ont, left_on = 'Term index', right_on = 'Term index', how = 'outer').merge(aro_name, left_on = 'Term_x', right_on = 'Accession', how = 'left')

import numpy as np
def select_similar_term(df):
    pairs = []
    for index, row in df.iterrows():
        
        if np.isnan(row['Similarity_y']):
            pairs.append(row[['Term index', 'Term_x', 'name_x']].tolist())
        elif np.isnan(row['Similarity_x']):
            pairs.append(row[['Term index', 'Term_y', 'name_y']].tolist())
        elif row['Similarity_x'] > row['Similarity_y']:
            pairs.append(row[['Term index', 'Term_x', 'name_x']].tolist())
        else:
            pairs.append(row[['Term index', 'Term_y', 'name_y']].tolist())
    
    term_df = pd.DataFrame(pairs, columns = ['Term index', 'Term', 'Name'])
    term_df.set_index('Term index', inplace = True)
    term_df.index.set_names('Term', inplace = True)
    return term_df
filtered_pan = select_similar_term(merged_pan)
filtered_ont2 = select_similar_term(merged_ont2)
ont2.update_node_attr(filtered_ont2)
pan_ont.update_node_attr(filtered_pan)

ndex_server = 'http://public.ndexbio.org'
ndex_user, ndex_pass = 'b101102109', '5mY87$747l'
url, _ = ont2.to_ndex(ndex_server=ndex_server, ndex_user=ndex_user, ndex_pass=ndex_pass,  layout="bubble-collect")
print(url)

url, _ = pan_ont.to_ndex(ndex_server=ndex_server, ndex_user=ndex_user, ndex_pass=ndex_pass,  layout="bubble-collect")
print(url)

print(ont2, pan_ont)


###### SAVE TO PICKLE #########
ont2.to_pickle('/home/hermuba/nas2/integrate_net/mero.annot.ddot')
pan_ont.to_pickle('/home/hermuba/nas2/integrate_net/pan.annot.ddot')