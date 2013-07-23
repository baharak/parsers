#!/bin/bash
OUT_FILE=U133-final
echo -e "ProbsetID\tSymbol\tRefSeq\tEntrezGene\tEnsembl_representative\tUniGene ID\tDescription" > "$OUT_FILE"
python excelreader.py HG-U133A.na33.annot.csv  >> "$OUT_FILE"

