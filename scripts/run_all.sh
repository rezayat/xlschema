source "scripts/common.sh"
package="python3 -W ignore -m xlschema from_uri"
xldir="data/xlsx"
files=$( ls $xldir/*.xlsx )

START=`date +%s`

section ">>> cleaning output"
rm -rf ./data/output/*

for f in $files; do
    section ">>> converting $f"
    $package --format $1 $f
    #echo "$package --method $1 $f"
done

END=`date +%s`

runtime "$((END-START))"
