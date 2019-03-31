gold=~/data0118/goldstandard/tf_intersectGO
sampled_gold=~/data0118/goldstandard/tf_intersectGO.smpl

# start an empty file
touch $sampled_gold

# feed first line, header to the output file
head -n 1 $gold > $sampled_gold

# sample from the second line
tail -n +2 $gold | shuf -n 100000 >> $sampled_gold
