
# conda rgi for py 3  is terrible

# before executing this script
# conda activate py27
# it's not possible to activate conda is a bash script

# run rgi including loose
rgi -t 'protein' -i $1 -o $2 -e YES

# then deactivate it
# conda deactivate
