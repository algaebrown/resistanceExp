# to dir containing .faa
cd ../data/genePredicted/resGeneTxt
ls -A1 | grep .faa | sed -e 's/\.txt//g' > oldList
mv oldList /home/hermuba/res

# difference
cd ../../../res
grep -F -x -v -f oldList ../data/allgenomelist.txt > needList

# run
cd /home/hermuba/data/genePredicted
source activate py27
cat /home/hermuba/res/needList | parallel rgi -t 'protein' -i {}.faa -o {}

# move to where it should be
#mv *.json ./resGeneJson
#mv *.txt ./resGeneTxt

#
source deactivate py27
