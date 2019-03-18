
outputfile=~/data/genome/all_genome_stat.tsv
for folder in ~/data/genome/genome_stat/*
do
tail $folder/transposed_report.txt -n 1 >> $outputfile
done
