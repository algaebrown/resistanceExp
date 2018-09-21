#!/bin/bash
# execute in the folder containing all target genome faa
# specify argument $1 = folder containing all target genome $2 = output folder

cd $1
pwd

for file in *.faa.gz;
do
    diamond makedb --in $file -d ${file%.faa.gz}
done

for file in *.dmnd
do diamond blastp --query /home/hermuba/data0118/cdhit/Escherichia0.70 --db ${file%.dmnd} --out $2${file%.dmnd} --outfmt 6 qseqid qlen sseqid slen sstart send qstart qend evalue bitscore stitle qtitle --verbose --threads 8
done
