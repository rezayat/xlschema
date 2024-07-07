source "scripts/common.sh"

section ">>> clean output files"
# rm -rf docs/_build
rm -rf data/output/*
rm -rf tests/data/output/*
rm -rf tests/data/logs/*.log

section ">>> cleaning testing files"
rm -rf .coverage .cache .hypothesis
