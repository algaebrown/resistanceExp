# input: all blastp outputs from one folder
# header: in dir /data0118/phylo_profile_refseq/faa this command was executed:
# for file in *.dmnd; do diamond blastp --query /home/hermuba/data0118/cdhit/Escherichia0.70 --db ${file%.*} --out /home/hermuba/data0118/phylo_profile_refseq/${file%.*} --outfmt 6 qseqid qlen ssequid slen sstart send qstart qend evalue bitscore stitle qtitle --verbose --threads 8; done

'''
Purpose: to make all blastp into a table containing:
1. rows = genes from pangenome
2. columns = refseq prtein faa (each genome)
3. value =
(1)*e value* of blastp;
(2)*gene name* to look back to gff for gene nieghboring

Potential problems:
1. two hits in one genome? which e-value/gene to pick?
2. no hit at all genome

'''
# test filename
filename = '/home/hermuba/data0118/phylo_profile_refseq/GCF_900492165.1_chr1_protein'
# 5338 hits, 1673 unique

# Step 1: read one blastp output file --> {gene: evalue, qseqid}
def read_blastp_out(f):
    with open(f) as f_handle:


        e_dict = {}
        hit_dict = {}

        for line in f_handle:
            attr = line.split('\t')

            # get gene, evalue, qseqid
            qseqid = attr[0]
            evalue = attr[8] # make it float
            sseqid = attr[2]

            e_dict[qseqid] = evalue
            hit_dict[qseqid] = sseqid

        return(e_dict, hit_dict)
# Step 2: add to the big tables (of size 10000*20000, is df not suitable?)
# Step 3: mutual information for the evalue table
