#!/bin/bash

for file in *
do
    awk '{print FILENAME (NF?"\t":"") $0}' $file >> ../eskape.tsv
done
