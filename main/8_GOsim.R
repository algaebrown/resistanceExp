library(ggplot2)
library(GOSemSim)

hsGO <- godata('org.Hs.eg.db', ont="BP")

######## INPUT #################
args = commandArgs(trailingOnly=TRUE)
#gold_anno_path = '/nas2/users/hermuba/network_hyperparam/selected_gene_anno.csv' # for selected benmark set only
gold_anno_path=args[1]
######## INPUT #################
outfile = args[2]



# dump rows without GO term
gold_anno = read.csv(gold_anno_path, sep = ',', header = TRUE)
go_nonempty = gold_anno[gold_anno$GO !='',]

print(nrow(go_nonempty))

split_go <-function(string){
    # Split the GO term in the csv
    vec = unlist(strsplit(string, "\'"))
    
    # remove unused
    vec = vec[vec !='}' & vec != ', ' & vec !='{']
    return(vec)
}

calc_GO_main <- function(rows){
    row1 = rows[1]
    row2 = rows[2]
    gostr1 <- as.character(go_nonempty[row1, "GO"])
    gostr2  <- as.character(go_nonempty[row2, "GO"])
        
    go1 = split_go(gostr1)
    go2 = split_go(gostr2)
        
    sim = mgoSim(go1, go2, semData=hsGO, measure="Wang", combine="BMA")
        
    name1 = go_nonempty[row1,"gene_id"]
    name2 = go_nonempty[row2,"gene_id"]
    if(name1<name2){
        return (c(name1, name2, sim))
        } else{
        return (c(name2, name1, sim))
    }
        
}

all_row_combinations = combn(c(1:nrow(go_nonempty)), 2)
write.table(t(apply(all_row_combinations, FUN = calc_GO_main, MARGIN = 2)), file=outfile)