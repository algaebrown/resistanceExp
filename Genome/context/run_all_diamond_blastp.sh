#!/bin/bash
# execute in the folder containing all target genome faa
for file in *.faa
do
    diamond makedb --in $file --db ${file%.*}
done

for file in *.dmnd
do diamond blastp --query /home/hermuba/data0118/cdhit/Escherichia0.70 --db ${file%.*} --out /home/hermuba/data0118/phylo_profile_refseq/${file%.*} --outfmt 6 qseqid qlen ssequid slen sstart send qstart qend evalue bitscore stitle qtitle --verbose --threads 8
done
