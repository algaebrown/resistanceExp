
cd /home/hermuba/data0118/cdhit/

for file in *rm_plasmid
do /home/yuwwu/bin/diamond/diamond blastp --query /home/hermuba/data0118/cdhit/$file --db /nas/hermuba/nr_0.9.11.dmnd --out /home/hermuba/data0118/cdhit/dmnd_nr/$file --outfmt 6 qseqid qlen sseqid slen sstart send qstart qend evalue bitscore stitle --verbose --threads 6 --max-target-seqs 1
done
