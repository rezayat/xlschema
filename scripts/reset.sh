START=`date +%s`

source scripts/clean.sh
source scripts/qcheck.sh
source scripts/coverage.sh
source scripts/docs.sh

END=`date +%s`

runtime "$((END-START))"
