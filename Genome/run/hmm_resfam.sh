# run hmmsearch for resfam
infile=~/data0118/cdhit/Escherichia0.70rm_plasmid

hmmsearch --tblout $infile-resfam /nas/hermuba/Resfams.hmm $infile
