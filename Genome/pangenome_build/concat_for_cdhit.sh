# to concat fasta file from genome_list, and faa
genome_list=/home/hermuba/data0118/genome_list/ecoli_rm_plasmid_1582

# faa path
faa_path=/home/hermuba/data/genePredicted/

# an empty file
touch /home/hermuba/data0118/ec_remove_plasmid_1580.faa
touch /home/hermuba/data0118/genome_list/ecoli_final

# 
final_list=/home/hermuba/data0118/genome_list/ecoli_final

# concat at the end of the file
for genome in `cat $genome_list`
do

    faa=$faa_path$genome.faa
if [ -e $faa ]
then
    cat $faa >> /home/hermuba/data0118/ec_remove_plasmid_1580.faa
    echo $genome >> $final_list
else
    echo $genome
fi

done
