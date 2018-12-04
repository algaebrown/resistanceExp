# run all file in to pfam
import os
def run_pfam(filename, inpath, outpath):
    os.chdir("/home/hermuba/PfamScan/")
    os.system("./pfam_scan.pl -fasta "+inpath +filename+" -outfile "+outpath+filename+" -dir ./pfam_db -cpu 16")

inpath = "/home/hermuba/data0118/cdhit/"
outpath = "/home/hermuba/data0118/pfam/"

threshold = ['0.70', '0.80', '0.95']
sps = ['Escherichia', 'Citrobacter', 'Acinetobacter', 'Enterobacter', 'Klebsiella', 'Pseudomonas', 'Salmonella']

for t in threshold:
    for s in sps:
        print(t+s)
        run_pfam(s+t, inpath, outpath)
