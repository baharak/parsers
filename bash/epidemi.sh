for d in MONOCYTIC-DIFFERENTIATION GRANULOCYTIC-DIFFERENTIATION  NO-MATURATION; do
    cd $d
    echo "entering $(pwd)"
    for f in F*; do
	echo $d/$f
        if ! cd $f; then
	    continue
	fi
        ../../compute-sim.sh
        cd ..
    done
    echo "leaving $(pwd)"
    cd ..
done
