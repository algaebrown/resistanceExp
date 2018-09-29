fname=$1
bash interproscan.sh --input ~/data0118/cdhit/split_ec/$fname --cpu 8 --goterm --pathways --seqtype p -o ~/data0118/interpro/${fname%.*} -f tsv
