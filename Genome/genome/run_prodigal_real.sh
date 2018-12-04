cd /home/hermuba/data/genome
cat /home/hermuba/data0118/genomeList/all | parallel $HOME/bin/Prodigal/prodigal -i {}.fna -o t.gbk -a {}.faa
