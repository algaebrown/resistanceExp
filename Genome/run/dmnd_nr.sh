

for file in *0.70
do diamond blastp --query /home/hermuba/data0118/cdhit/$file --db /nas/hermuba/nr_0.19.120 --out /home/hermuba/data0118/cdhit/dmnd_nr/$file --outfmt 6 qseqid qlen sseqid slen sstart send qstart qend evalue bitscore stitle qtitle --verbose --threads 1 --max-target-seqs 1
done
