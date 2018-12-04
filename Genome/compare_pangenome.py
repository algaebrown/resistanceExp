#
supra_path = '/home/hermuba/data0118/cdhit/'
db_path = '/home/hermuba/data0118/cdhit/blast_db/'

# makeblastdb
def make_db(name):
    os.system('makeblastdb -in ' + supra_path + name +' -input_type fasta -dbtype prot -out '+db_path+name)

# blast
def run_blast(query, db_name):
    os.system('blastp -query ' + supra_path + query +' -db ' + db_path + db_name + ' -evalue 1e-5 -outfmt 6 -max_target_seqs 1 >'+ supra_path + 'blast_two/' + query+db_name)

threshold = ['0.70', '0.80', '0.95']
organism = ['Escherichia', 'Klebsiella', 'Acinetobacter']

for t in threshold:
    for o in organism:
        make_db(o+t)

for t in threshold:
    run_blast('Escherichia'+t, 'Klebsiella'+t)
    run_blast('Escherichia'+t, 'Acinetobacter'+t)
    run_blast('Acinetobacter'+t, 'Klebsiella'+t)
