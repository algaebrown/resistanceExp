#!/bin/bashx
# $1=output file
# $2=folder containing blast result

for file in *
do
    awk '{print FILENAME (NF?"\t":"") $0}' $file >> $1
done
