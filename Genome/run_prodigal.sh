cd /home/hermuba/data/genome-gogo
cat /home/hermuba/data/allgenomelist.txt | parallel $HOME/bin/Prodigal/prodigal -i {}.fna -o t.gbk -a {}.faa
