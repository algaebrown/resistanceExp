# load blast result


# accessing uniprot ID converter throught gi and accession numbero
from biosevices.uniprot import Uniport
u = UniProt(verbose=False)
u.mapping(fr="ACC+ID", to="ID", query='P43403') # to uniprot ID
