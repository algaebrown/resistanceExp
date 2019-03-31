folder=~/data0118/interpro/
interpro_out=~/data0118/interpro/all

# add header
head -n 1 ~/data0118/interpro/myseq0 > $interpro_out

# concat all of them
for file in $folder*
do
    tail -n +2 $file >> $interpro_out
done
