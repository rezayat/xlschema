source scripts/common.sh
section ">>> coverage"
pytest --cov-report html:docs/coverage --cov=xlschema
