gold=$1 # input file
sampled_gold=$2 # output file
n_sample=$3 # number of lines to sample

# start an empty file
touch $sampled_gold

# feed first line, header to the output file
head -n 1 $gold > $sampled_gold

# sample from the second line
tail -n +2 $gold | shuf -n $n_sample >> $sampled_gold
