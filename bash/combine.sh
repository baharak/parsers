#!/bin/bash
OUT_FILE=final

print_header() {
    echo -e "ProbsetID\tSymbol\tRefSeq\tEntrezGene\tEnsembl_representative\tUniGene ID\tDescription"
}

python combiner.py '1' '1 2 3 4 5 6 7' U133/U133-final gnf/gnf-final | sort > tmp

print_header > "$OUT_FILE"
cat tmp | \
#join -t $'\t' <(sort probsetIds) tmp | \
    sed 's/'$'\t'$'\t''/'$'\t''-'$'\t''/g' | \
    sed 's/'$'\t'$'\t''/'$'\t''-'$'\t''/g' | \
    sed 's/'$'\t'$'\t''/'$'\t''-'$'\t''/g' | \
    sed 's/'$'\t'$'\t''/'$'\t''-'$'\t''/g' | \
    sed 's/'$'\t'$'\t''/'$'\t''-'$'\t''/g' | \
    sed 's/'$'\t'$'\t''/'$'\t''-'$'\t''/g' | \
    sed 's/'$'\t'$'\t''/'$'\t''-'$'\t''/g' | \
    sed 's/'$'\t''$/'$'\t''-/g' >> "$OUT_FILE"

#tail -n +2 "$OUT_FILE" | cut -f1 > probsetIds-matched
#comm -23 <(sort probsetIds) probsetIds-matched | \
#    awk '{printf "%s\t-\t-\t-\t-\t-\t-\n", $0}' >> "$OUT_FILE"

print_header > "$OUT_FILE"-ordered
echo "single line" > oneliner
python orderer.py '1' '1 2 3 4 5 6 7' <(cat oneliner probsetIds) "$OUT_FILE" >> "$OUT_FILE"-ordered
