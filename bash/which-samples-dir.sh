dir=$(echo '/home/bsaberid/Dropbox/research/flowCy/wallace-data/PatientRaw/' | sed -r -e 's/\//\\\//g')
suffix=$1
shift
./which-samples.sh "$@" | sed -r -e 's/.*/'"$dir""&$suffix/" -e "s/ /\\\\ /g"
