import os
import sys
import pandas as pd
from optparse import OptionParser
''' 
Take excel file downloaded from patric as input
download .fna from PATRIC FTP 
Excel filtered by 1. Antimicrobial resistance must be either RIS 2. Host: Homo sapiens 3. Genome quality good
'''

parser = OptionParser()
parser.add_option("-f", "--folder", dest="genome_path",
                  help="folder to contain genomes downloaded")
parser.add_option("-e", "--excel", dest="excel",
                  help="Excel spreadsheet downloaded from PATRIC database portal. url: https://www.patricbrc.org/view/Taxonomy/561#view_tab=genomes")

(options, args) = parser.parse_args()

# a script to download genomes
genome_path = options.genome_path
genome_list = options.excel

df = pd.read_excel(genome_list, dtype = {'Genome ID':str})
id_list = df['Genome ID']

for number, i in enumerate(id_list):
    if os.path.isfile(os.path.join(genome_path, '{}.fna'.format(i))):
        pass # already downloaded

    else:
        os.system("wget ftp://ftp.patricbrc.org/genomes/{}/{}.fna -P {}".format(i,i,genome_path))
    if number>0 and number%100 == 0:
        print('Download {} out of {}'.format(number, len(id_list)))
