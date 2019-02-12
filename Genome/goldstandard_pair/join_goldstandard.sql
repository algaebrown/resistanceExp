
SELECT f.gene_one, f.gene_two
FROM full_net f
LEFT JOIN tf_intersect_pathway g2
ON (f.gene_one = g2.gene_one AND f.gene_two = g2.gene_two) OR (f.gene_one = g2.gene_two AND f.gene_two = g2.gene_one)

LEFT JOIN tf_intersect_go g1
ON (f.gene_one = g1.gene_one AND f.gene_two = g1.gene_two) OR (f.gene_one = g1.gene_two AND f.gene_two = g1.gene_one)

LEFT JOIN refseq_ordinary_40 r
ON (f.gene_one = r.gene_one AND f.gene_two = r.gene_two) OR (f.gene_one = r.gene_two AND f.gene_two = r.gene_one)

LEFT JOIN eskape_mu e
ON (f.gene_one = e.gene_one AND f.gene_two = e.gene_two) OR (f.gene_one = e.gene_two AND f.gene_two = e.gene_one)

LEFT JOIN domain d
ON (f.gene_one = d.gene_one AND f.gene_two = d.gene_two) OR (f.gene_one = d.gene_two AND f.gene_two = d.gene_one)

LEFT JOIN string_db s
ON (f.gene_one = s.gene_one AND f.gene_two = s.gene_two) OR (f.gene_one = s.gene_two AND f.gene_two = s.gene_one)

# error message: FULL JOIN is only supported with merge-joinable or hash-joinable join conditions

# explaination: https://postgrespro.com/list/thread-id/1230535 OR statment
# it's some problem with the join algorithm: https://www.pgcon.org/2017/schedule/attachments/455_pgcon-2017-hash-joins.pdf
# too complicated. I'm not interested

# solution 1: union all : https://stackoverflow.com/questions/47405732/why-does-postgresql-throw-full-join-is-only-supported-with-merge-joinable-or-ha
# solution 2: generate a list of all possible combinations and then left join all results
