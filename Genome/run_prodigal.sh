cd /home/hermuba/data/genome
cat /home/hermuba/data0118/genomeList/all | parallel wget ftp://ftp.patricbrc.org/patric2/genomes/{}/{}.fna
