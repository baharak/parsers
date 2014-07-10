# author: Baharak Saberidokht
#!/bin/bash
[ -z "$MIN_ISECT" ] && MIN_ISECT=2
[ $# -ge 1 ] && s0="$1" || s0=sample # compare against file "sample" by default

get_ids() {
    echo $@ | sed 's/, .*//' | tr ' ' '\n' | sort
}

get_coords() {
    echo $@ | sed 's/.*, //' | tr ' ' '\n'
}

for s in sample-*; do
    echo "Comparing: $s0 vs $s ..." >&2
    res=results/$s.res  # write results to: sample-<n>.result
    mkdir -p $(dirname "$res")
    >$res	# clear the file (since we append later)
    isect_cnt=0	# number of isect (by max isect) >= MIN_ISECT
    isect_max=0	# currently best isect (by max isect)
    edist_min=1000000  # currently best edist (by min edist)
    best_by_isect=
    best_by_edist=
    while read s0_line; do
	[ -z "$s0_line" ] && continue  # skip empty lines
	tmp=compute-sim.temp
	trap 'rm -f $tmp' EXIT
	while read s_line; do
	    [ -z "$s_line" ] && continue  # skip empty lines
	    isect=$(comm -12 <(get_ids $s0_line) <(get_ids $s_line) | wc -l)
	    edist=$(paste -d'-' <(get_coords $s0_line) <(get_coords $s_line) |\
		sed -r 's/.*/(&)^2/' | paste -sd+ |\
		sed -r 's/.*/sqrt(&)/' |\
		bc -l)
	    echo "$isect $edist"
	done <$s >$tmp

	# print all pairs <isect> <edits sorted by max isect/edist to stderr
	max_by_isect=$(sort -rnk 1 $tmp | head -n 1)
	min_by_edist=$(sort -nk 2 $tmp | head -n 1)
	echo "$max_by_isect $min_by_edist" >>$res

	# update max isect and corresponding edist
	isect=$(echo $max_by_isect | cut -d' ' -f1)
	(( $isect >= $MIN_ISECT )) && let ++isect_cnt  # update the counter
	if (( $isect > $isect_max )); then
	    best_by_isect="$max_by_isect"
	    isect_max=$isect
	fi
	edist=$(echo $min_by_edist | cut -d' ' -f2)
	if (( $(echo $edist '<' $edist_min | bc -l) == 1 )); then
	    best_by_edist="$min_by_edist"
	    edist_min=$edist
	fi
    done <$s0
    echo "$s0 $s $isect_cnt $best_by_isect $best_by_edist"
done | tee summary
