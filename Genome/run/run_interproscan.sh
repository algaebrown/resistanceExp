# remove asterisk
infile=$1 # representing gene clusters
tmpdir=$2
outf=$3

mkdir $tmpdir

# remove aster sticks for interproscan
cat $infile | tr -d "*" > $infile.rm_aster

# cut large fasta into ten pieces (1000 seqs each)

awk 'BEGIN {n_seq=0;} /^>/ {if(n_seq%1000==0){file=sprintf("myseq%d.faa",n_seq);} print >> file; n_seq++; next;} { print >> file; }' < $infile.rm_aster

# move all split faa files into tmpdir
mv myseq* $tmpdir



# run interproscan one by one
cd $tmpdir

for fname in ./*faa
do
    outputname=$(basename $fname)
    bash ~/bin/interproscan-5.48-83.0/interproscan.sh --input $fname --cpu 8 --goterm --pathways --seqtype p -o ${outputname%.*}.out -f tsv
done

# concat all interproscan output pieces




# concat all of them
for file in ./*.out
do
    cat $file >> $outf
done

