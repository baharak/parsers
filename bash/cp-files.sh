for f in F*; do
    echo $f
    cd $f
    cp formatted-MONOCYTIC-DIFFERENTIATION ../../aml-output/MONOCYTIC-DIFFERENTIATION/$f
    mv ../../aml-output/MONOCYTIC-DIFFERENTIATION/$f/formatted-MONOCYTIC-DIFFERENTIATION ../../aml-output/MONOCYTIC-DIFFERENTIATION/$f/sample
    cp formatted-GRANULOCYTIC-DIFFERENTIATION ../../aml-output/GRANULOCYTIC-DIFFERENTIATION/$f
    mv ../../aml-output/GRANULOCYTIC-DIFFERENTIATION/$f/formatted-GRANULOCYTIC-DIFFERENTIATION ../../aml-output/GRANULOCYTIC-DIFFERENTIATION/$f/sample
    cp formatted-NO-MATURATION ../../aml-output/NO-MATURATION/$f
    mv ../../aml-output/NO-MATURATION/$f/formatted-NO-MATURATION ../../aml-output/NO-MATURATION/$f/sample
    cd ..
done

