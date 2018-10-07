 select t.e from (select to_char(evalue,'EEEE') as e,dense_rank() over (order by evalue ASC) as dense_rank from blastp_out_max_evalue) as t where t.dense_rank = 2
