# make blastp db
diamond makedb --in /home/hermuba/data0118/map_to_exist_net/EcoliNet/ecoli_proteome.fasta --db ecoli_proteome

# diamond against it
diamond blastp --query ~/data0118/cdhit/Escherichia0.70rm_plasmid --db ecoli_proteome.dmnd --outfmt 6 --out ec_rmplasmid_ecolinet
