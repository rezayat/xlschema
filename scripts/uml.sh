source scripts/common.sh

WORK=/work
DOCK_SRC=${WORK}/docs/uml
DOCK_DST=${WORK}/docs/_static/uml
SRC=./docs/uml
DST=./docs/_static/uml
NAMES=$(ls ${SRC}/*.puml)

function gen_uml {
  name=$(basename $1 .puml)
  echo "$1 -> ${DST}/${name}.$2"
  docker run -it --rm \
    -v `pwd`:${WORK} \
    -w ${WORK} \
    img-toolkit \
    java -jar /app/plantuml.jar -t$2 ${DOCK_SRC}/${name}.puml
  mv ${SRC}/${name}.$2 ${DST}/${name}.$2
}

section ">>> generating uml"
for f in $NAMES; do
  # gen_uml $f png
  gen_uml $f svg
done
