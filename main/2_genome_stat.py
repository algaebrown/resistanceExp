# a script to check genome status; filter for better quality genome
# Input: PATRIC genome excel file
# Output: genome statistics file
import os
import pandas as pd
import sys
import subprocess
from optparse import OptionParser
parser = OptionParser()

parser.add_option("-s", "--stat", dest="stat_tsv",
                  help="folder with quast output")
parser.add_option("-p", "--prodigal", dest="prodigal_count",
                  help="file_with_prodigal_count")
parser.add_option("-e", "--excel", dest="excel",
                  help="Excel spreadsheet downloaded from PATRIC database portal. url: https://www.patricbrc.org/view/Taxonomy/561#view_tab=genomes")
parser.add_option("-o", "--out", dest="outf",
                  help="output genome_stat.csv")
(options, args) = parser.parse_args()


# read PATRIC file
df = pd.read_excel(options.excel, dtype = {'Genome ID':str})
id_list = df['Genome ID']



# join quast information with PATRIC genome stats
quast_df = pd.read_csv(options.stat_tsv, sep="\t", dtype = {'Assembly':str}) # index is genome id
quast_df.set_index('Assembly', inplace = True)
df.set_index('Genome ID', inplace = True) # patric

# merge quast and PATRIC information
merged = pd.merge(quast_df, df[['Sequencing Status', 'Contigs','Genome Length','GC Content','PATRIC CDS','RefSeq CDS']], left_index = True, right_index = True)


prodigal_count = pd.read_csv(options.prodigal_count, sep = ' ', names = ['fname', 'count'])
prodigal_count['Genome ID'] = prodigal_count['fname'].str.split('/', expand = True)[1].str.replace('.faa', '')
merged['prodigal_CDS'] = merged.index.map(prodigal_count.set_index('Genome ID')['count'])

# select genomes
# not plasmid, 
# number of genes
merged['include'] = True
merged.loc[merged['prodigal_CDS']<merged['prodigal_CDS'].median()*0.6, 'include'] = False
merged.loc[merged['Sequencing Status']=='Plasmid', 'include'] = False
print('plan to include {} out of {} genomes'.format(merged['include'].sum(), len(id_list)))

            
merged.to_csv(options.outf)
print('Genome stat saved to {}'.format(options.outf))
    
        