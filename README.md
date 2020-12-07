# Pangenomic View on Antibiotic Resistance
Lab notebook the following research:

1. A pan-genome-based machine learning approach for predicting antimicrobial resistance activities of the Escherichia coli strains. HL Her, YW Wu. Bioinformatics 34 (13), i89-i95(2018)
2. PangenomeNet: A pan-genome-based functional network provide mechanistic view on Meropenem Resistome for Escherichia coli strains. Hsuan-Lin Her, Po-Ting Lin, and Yu-Wei Wu. (In preperation)

# File structure:
1. in **Drug** folder, there are codes for TMACC, CHEBI, all kinds of drug database and chemical descriptor
2. in **Genome** folder, codes are about pan-genome construction,
    - `annotate_parser` contain functions to parse annotations from CARD, BLAST, COG, HMMer, pFAM and REsfam
    - `context` folder contains functions and scripts to construct co-inheritance network
    - `genome` folder contains scripts to download genome from PATRIC, and calculate genome statistics
    - `goldstandard_pair` folder contains scripts to validate networks, generate gold-standard gene pairs.
    - `pangenome_annotation` folder contains scripts to annotation gene clusters from the pan-genome
    - `pangenome_build` contains scripts used to call CD-hit
    - `pangenome_intrinsic_info` contains scripts to calculate pan-genome statistics
    - `string` contains parsing EcoliNet, Mentha and STRING network
3. in **MIC** folder, codes are mainly related to CLSI re-annotation for resistance phenotypes
4. in **Model** folder, codes are all about training svm and nb models
5. `compare_scoary` contains code that compares [1] to Scoary.
5. the **Visulazation folder** contains all sorts of jupyter notebook, mainly used to plot
6. `cleanData.py` selects data that fits our need (with MIC instead of disk diffusion, the right species ...etc)
7. in **network_analysis** contain codes for powerlaw regression
