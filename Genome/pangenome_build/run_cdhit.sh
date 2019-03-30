# $1: input file=concat .faa; $2 outputfile: ~/data0118/cdhit/XX
cd-hit -i $1 -o $2 -T 6 -c 0.7 -d 0 -M 7000

# organize
mv ~/data0118/cdhit/*.clstr ~/data0118/cdhit/clstr/
