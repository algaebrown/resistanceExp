# input blastp outfmt 6
blast_result = "/home/hermuba/blastp_1001.txt"

# setup entrez
from Bio import Entrez
Entrez.email = "b101102109@tmu.edu.tw"

# dataframe
import pandas as pd
df = pd.DataFrame(columns = ['accession', 'identity', 'gi', 'title'])

with open(blast_result) as f:
    for line in f:
        accession = line.split('\t')[1]
        gene_header = line.split('\t')[0]
        identity = float(line.split[2])

        # search entrez for idlist
        handle = Entrez.esearch(db = "protein", term = accession)
        record = Entrez.read(handle)
        ID = record['IdList'][0]

        # search for summary
        handle = Entrez.esummary(db = "protein", id = ID)
        record = Entrez.read(handle)
        title = record[0]['Title']

        # save into df
        df.loc[gene_header, :] = [accession, identity, ID, title]
