source scripts/common.sh

source scripts/uml.sh


section ">>> build docs"
make -C docs clean
make -C docs html
