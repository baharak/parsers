cat samples-reading.csv | tr '\n' '\t' | sed -r -e 's/\s+/ /g' -e 's/[0-9]{11}/\n&/g' |  tail -n +2 > samples-reading-merged
sed -r 's/([0-9]{11}).*POPULATION EXPRESSES ([^.]*).*THIS IS CONSISTENT WITH ACUTE MYELOID LEUKEMIA WITH ([^.]*).*\..*/\1|\3|\2|\3/g' samples-reading-merged | sed -r \
    -e 's/^([^|]+\|[^|]+\|[^|]+\|[^|]+[^0-9]) AND /\1\|/g' \
    -e 's/(.*)(BOTH|SOME) ([^|]+)/\1\3 DIFFERENTIATION/' \
    -e 's/GRANULOCYTIC\|MONOCYTIC MATURATION$/GRANULOCYTIC MATURATION|MONOCYTIC MATURATION/' \
    -e 's/(MONOCYTIC)\|((GRANULOCYTIC) (DIFFERENTIATION))$/\1 \4|\3 \4/' \
    -e 's/(GRANULOCYTIC)\|((MONOCYTIC) (DIFFERENTIATION))$/\1 \4|\3 \4/' \
> samples-all

egrep '\|' samples-all > samples-ok
egrep -v '\|' samples-all | grep -v 'WITH ACUTE MYELOID LEUKEMIA\.' | sed -r 's/([0-9]{11}) /\1|/g' > samples-partial
egrep -v '\|' samples-all | grep 'WITH ACUTE MYELOID LEUKEMIA\.' | sed -r 's/([0-9]{11}) /\1|/g' > samples-nodisease
