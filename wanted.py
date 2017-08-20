# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 20:43:15 2017
needed genome
@author: Charl
"""

# compare what we already have with the new list
data_dir = 'data'
entero_data = 'PATRIC_genome_amr_20170708.xlsx'
acineto_data = 'PATRIC_genone_amr_acineto_20170716.xlsx'
pseudo_data = 'PATRIC_genome_amr_pseudo_20170716.xlsx'
old_data = 'combineMICtoARO.xlsx'


# load them
import pandas as pd
entero = pd.read_excel(data_dir + '/' + entero_data)
acineto = pd.read_excel(data_dir + '/' + acineto_data)
pseudo = pd.read_excel(data_dir + '/' + pseudo_data)
old = pd.read_excel(data_dir + '/' + old_data)


def ab(a,b):
    return(a+b)

# combine all new data
new = pd.concat([entero,acineto,pseudo],ignore_index = True)

# remove duplicates of genome ID
diff = set(list(new['Genome ID'])).difference(set(list(old['ID'])))

wanted = list(diff)
