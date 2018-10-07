CREATE TABLE joined_data ASb5
SELECT tf_intersect.gene_one, tf_intersect.gene_two, tf_intersect.goldstandard, eskape_mu.mutual_info, eskape_mu.nrm_mutual
FROM eskape_mu
FULL JOIN tf_intersect
ON (tf_intersect.gene_one = eskape_intersect.gene_one AND tf_intersect.gene_two = eskape_intersect.gene_two) OR (tf_intersect.gene_one = eskape_intersect.gene_two AND tf_intersect.gene_two = eskape_intersect.gene_one)
