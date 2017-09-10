# to dir containing .faa
#cd ../data/genePredicted
#ls -A1 | grep .faa | sed -e 's/\.faa//g' > oldList
#mv oldList /home/hermuba/res

# difference
#cd ../../res
#diff ../data/allgenomelist.txt oldList > needList

# run
cd /home/hermuba/data/genePredicted
source activate py27
cat /home/hermuba/data/allgenomelist.txt | parallel rgi -t 'protein' -i {}.faa -o {}

# move to where it should be
mv *.json ./resGeneJson
mv *.txt ./resGeneTxt

#
source deactivate py27




