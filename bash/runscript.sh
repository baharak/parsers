#!/bin/bash
#cd enrichmentTest

function run {
        if [[ "$dir3" == "$1" ]]
            then
                 d="$dir/$dir2/$dir3"   
                 if [ -e "$d" ]; then
                     cd "$d"  
                     find "$PWD" -name '*.tsv' | xargs -I {}  python ../../../GestaltParser.py {} "$2" #run the python script
                     cd -
                 fi 
                   
         fi
}

for dir in blood brain ganglian testis; do
    for dir2 in CG_H CG_Y HS; do
        for dir3 in Disease GO KEGG; do    
            #run  "Disease" "disease"
            #run "GO" "biological process"
            #run "GO" "cellular component"
            #run "GO" "molecular function"
            run "KEGG" "KEGG pathway"
                              
        done
    done
    
done
exit   


  
