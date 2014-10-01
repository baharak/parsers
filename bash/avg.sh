# for f in F*.txt; do f=${f%.*}; awk 'NR%5==1' $f.txt > $f.csv; done
for f in F*.csv; do f=${f%.*}; echo -n $f
    for c in $(seq 1 6);
    do
	col_sum=$(tail -n +2 $f.csv |  cut -d',' -f$c \
	    | grep -v 'NaN' \
	    | tr '\n' '+')0
	n=$(echo $col_sum | grep -o '+' | wc -l) # count +s
	col_sum=$(echo $col_sum | bc -l)
	echo -n ",=$col_sum/$n"
    done
    echo
done > avg-output.csv

