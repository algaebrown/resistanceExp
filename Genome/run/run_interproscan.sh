# remove asterisk
infile=~/data0118/cdhit/Escherichia0.70rm_plasmid
cat $infile | tr -d "*" > $infile-rm_aster

# cut into ten pieces

awk 'BEGIN {n_seq=0;} /^>/ {if(n_seq%1000==0){file=sprintf("myseq%d.faa",n_seq);} print >> file; n_seq++; next;} { print >> file; }' < $infile-rm_aster

mv myseq* ~/data0118/cdhit/split_ec/

rm $infile-rm_aster


# run interproscan one by one
for fname in ~/data0118/cdhit/split_ec/*faa
do
    outputname=$(basename $fname)
    bash ~/bin/interproscan-5.34-73.0/interproscan.sh --input $fname --cpu 8 --goterm --pathways --seqtype p -o ~/data0118/interpro/${outputname%.*} -f tsv
done
