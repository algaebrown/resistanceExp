# make blastp db
diamond makedb --in ~/data0118/map_to_exist_net/mentha.fasta --db mentha

# diamond against it
diamond blastp --query ~/data0118/cdhit/Escherichia0.70rm_plasmid --db mentha.dmnd --outfmt 6 --out ec_rmplasmid_mentha
