awk -F "\t" '$12=="Complete Genome" && $11=="latest"{print $20}' $1 > ftpdirpaths
awk 'BEGIN{FS=OFS="/";filesuffix="protein.faa.gz"}{ftpdir=$0;asm=$10;file=asm"_"filesuffix;print ftpdir,file}' ftpdirpaths > ftpfilepaths

for file in $(cat ftpfilepaths);
do
wget $file -P $2
done
