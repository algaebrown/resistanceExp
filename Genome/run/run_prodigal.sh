# to run prodigal from genome_list, and fna
genome_list=/home/hermuba/data0118/genome_list/ecoli_rm_plasmid_1582

# faa path
faa_path=/home/hermuba/data/genePredicted/

# fna path
fna_path=/home/hermuba/data/genome/

# run per genome
for genome in `cat $genome_list`
do

    prodigal -i $fna_path$genome.fna -o $faa_path.$genome.faa -p meta
done
