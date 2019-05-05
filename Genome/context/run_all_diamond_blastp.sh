#!/bin/bash
# execute in the folder containing all target genome faa
# specify argument $1 = folder containing all target genome $2 = output folder $3 cdhit repr gene

cd $1
pwd

for file in *.faa
do diamond makedb --in $file --db ${file%.faa}
done

for file in *.dmnd
do diamond blastp --query $3 --db ${file%.dmnd} --out $2${file%.dmnd} --outfmt 6 qseqid qlen sseqid slen sstart send qstart qend evalue bitscore stitle --verbose --threads 8
done
