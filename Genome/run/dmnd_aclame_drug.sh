file=/home/hermuba/data0118/cdhit/Escherichia0.70rm_plasmid

# run ACALME: mobile elements in pan-genome; diamond
/home/yuwwu/bin/diamond/diamond blastp --query $file --db /nas/hermuba/aclame_mobile_element.dmnd --out $file-aclame --outfmt 6 qseqid qlen sseqid slen sstart send qstart qend evalue bitscore stitle --verbose --threads 6 --max-target-seqs 1 -e 1e-5

# run drug target:
/home/yuwwu/bin/diamond/diamond blastp --query $file --db /nas/hermuba/ARO3000708.dmnd --out $file-drug_target --outfmt 6 qseqid qlen sseqid slen sstart send qstart qend evalue bitscore stitle --verbose --threads 6 --max-target-seqs 1 -e 1e-5
