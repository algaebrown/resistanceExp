
# input file
repr_faa=$1
outdir=$3
name=$2

# RUN CARD
source ~/miniconda3/etc/profile.d/conda.sh
# remove aster sticks for interproscan and CARD RGI
cat $repr_faa | tr -d "*" > $repr_faa.rm_aster

conda activate card
rgi main -t 'protein' -i $repr_faa.rm_aster -o $outdir$name.card 
conda deactivate

#os.system('bash /home/hermuba/resistanceExp/Genome/run/card_for_rep_gene.sh ' + '/home/hermuba/data0118/cdhit/' + generic_fname + ' /home/hermuba/data0118/cdhit/card/' + generic_fname)

# RUN COG
echo $repr_faa > cog_flist # specialized input for this script
perl ~/bin/COGmapper/map_COG.pl cog_flist $outdir$name.cog
rm cog_flist


# run resfam
hmmsearch --tblout $outdir$name.resfam /nas/hermuba/Resfams.hmm $repr_faa
#os.system('bash ~/resistanceExp/Genome/run/hmm_resfam.bash')

# run aclame
# diamond makedb --in /nas/hermuba/aclame_proteins_all_0.4.fasta -d /nas2/users/hermuba/dmnd_db/aclame_mobile_element
# run ACALME: mobile elements in pan-genome; diamond
/home/yuwwu/bin/diamond/diamond blastp --query $repr_faa \
--db /nas2/users/hermuba/dmnd_db/aclame_mobile_element.dmnd \
--out $outdir$name.aclame \
--outfmt 6 qseqid qlen sseqid slen sstart send qstart qend evalue bitscore stitle \
--verbose --threads 6 --max-target-seqs 1 -e 1e-5

# run drug target:
# diamond makedb --in /nas/hermuba/[ARO:3000708]-2019-03-18T05:39:47+00:00-protein.fasta -d /nas2/users/hermuba/dmnd_db/ARO3000708
/home/yuwwu/bin/diamond/diamond blastp --query $repr_faa \
--db /nas2/users/hermuba/dmnd_db/ARO3000708.dmnd \
--out $outdir$name.drug_target \
--outfmt 6 qseqid qlen sseqid slen sstart send qstart qend evalue bitscore stitle \
--verbose --threads 6 --max-target-seqs 1 -e 1e-5

# run diamond for nr # nr.gz at /home2/sequence_db/nr/nr.gz
/home/yuwwu/bin/diamond/diamond blastp --query $repr_faa \
--db /nas2/users/hermuba/dmnd_db/nr.dmnd \
--out $outdir$name.nr \
--outfmt 6 qseqid qlen sseqid slen sstart send qstart qend evalue bitscore stitle \
--verbose --threads 6 --max-target-seqs 1

# run uniref50
/home/yuwwu/bin/diamond/diamond blastp --query $repr_faa \
--db /nas2/users/hermuba/dmnd_db/uniref50.dmnd \
--out $outdir$name.uniref \
--outfmt 6 qseqid qlen sseqid slen sstart send qstart qend evalue bitscore stitle \
--verbose --threads 6 --max-target-seqs 1 -e 1e-5

# run interproscan
tmpname=interproscan_splits
mkdir $outdir$tmpname
tmpdir=$outdir$tmpname/
~/resistanceExp/Genome/run/run_interproscan.sh $repr_faa $tmpdir $outdir$name.interpro
