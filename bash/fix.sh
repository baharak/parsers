#!/bin/bash
GNF_FILE=deletion66gnf1h.annot2007.tsv
ENST_FILE=EnsT2EnsG.txt 
OUT_FILE=gnf-final
mid_computedone=1coldata
mid_computedsec=1colcomputed

echo -e "ProbesetID\tSymbol\tRefSeq\tEntrezGene\tEnsembl_representative\tUniGene ID\tDescription" > "$OUT_FILE"
python ../U133/aggregator.py '1' \
    "$GNF_FILE" '1 2 3 4 5 6 7 8 9 10' \
    "$ENST_FILE" '11 9' \
    '9' '1 7 3 6 11 4 8' | \
    grep -v 'obsoleted by Celera' >> "$OUT_FILE"

    cut -f1 deletion66gnf1h.annot2007.tsv > "$mid_computedone"
    cut -f1 gnf-final > "$mid_computedsec"	

    comm -23  <(sort 1coldata) <(sort 1colcomputed)| \
    awk '{printf "%s\t-\t-\t-\t-\t-\t-\n", $0}' >> "$OUT_FILE"   

