# convert gi to uniprot id by connecting to uniprot API

# import blast parsed result



## bypass the first step, use uniprot id converter web

### the reviewed 4577
uniprot_id_path = '/home/hermuba/data0118/uniprot/'
rev_id = 'uniprot_rev.list'

# a function to convert file sep = '\n' to a list
def newline_list(filename):

    with open(uniprot_id_path + filename) as f:
        l = f.readlines()
    clean_l = [i.replace('\n', '') for i in l]
    return(clean_l)
# uniprot id to EVEX ggpid `search_ggp`
import requests
import xml.etree.ElementTree as ET
def uniprot_ggpid(uniprot_id):
    """
    input: uniport_id
    output: ggpid, gene synonoym
    """
    base_url = 'http://evexdb.org/api/v001/search_ggp/'
    payload = {'searchType': 'uniprot',
               'family': 'egenomes',
               'term': uniprot_id}

    r = requests.get(base_url, params = payload)

    root = ET.fromstring(r.text)

    try:
        ggpid = root[1][0][0].text
        synonym = root[1][0][1].text

        return(ggpid, synonym)
    except IndexError:
        print('uniport id not found in evex')
        return(0,0) # if no result, will get 0
# save uniprot_id, ggpid, synonym to dataframe
import pandas as pd
#evex_id = pd.DataFrame(columns = ['ggpid', 'synonym'])
evex_id = pd.read_pickle(uniprot_id_path + 'evex_id_df')
u_list = newline_list(rev_id)
for u_id in u_list:
    if u_id not in evex_id.index:
        ggp, syn = uniprot_ggpid(u_id)

        evex_id.loc[u_id] = [ggp, syn]
    # evex_id.to_pickle(uniprot_id_path+'name_on_it') ################### modify to save properly

# conbine all gppid list and feed into `fetch_network`
def ggpid_concat(evex_id_df):
    unique_no_empty = evex_id_df.loc[evex_id_df['ggpid'] != 0]['ggpid'].unique()
    concat_ggpid = ''
    for ggp in unique_no_empty:
        concat_ggpid = concat_ggpid + ',' + ggp

    return(concat_ggpid[1:])

# fetch_network
def fetch_evex_network(ggpid_list):


    url = 'http://evexdb.org/api/v001/fetch_network/?ggpIdList=' + ggpid_list + '&family=egenomes'
    r = requests.get(url)
    return(r)

def net_xml_df(r):
    df = pd.DataFrame(columns = ['source', 'sourceName', 'target', 'targetName', 'coarseType', 'refinedType', 'coarsePolarity', 'refinedPolarity', 'event', 'direction', 'averageConfidence', 'negation', 'speculation'])
    root = ET.fromstring(r.text)
    result = root[1]
    for i in range(len(result)):
        link = result[i]
        print(link.text)
        attr_list = []
        for j in range(13):
            attr_list.append(link[j].text)
        df.loc[i] = attr_list

    return(df)
