# make blastp db
diamond makedb --in 511145.protein.sequences.v11.0.fa.gz --db string

# diamond against it
diamond blastp --query ~/data0118/cdhit/Escherichia0.70rm_plasmid --db string.dmnd --outfmt 6 --out ec_rmplasmid_string
