cut -d'|' -f4- samples-ok | tr '\|' '\n' | sort | uniq -c | sort -nr
