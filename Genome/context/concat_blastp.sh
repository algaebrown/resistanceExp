#!/bin/bashx

for file in *
do
    awk '{print FILENAME (NF?"\t":"") $0}' $file >> $1
done
