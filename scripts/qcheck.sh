source scripts/common.sh

section ">>> pylint"
pylint xlschema

section ">>> flake8"
flake8 xlschema

section ">>> radon"
radon cc --ignore "tests,docs,resources" --min C xlschema

section ">>> proselint"
DOCS="README.md docs/userguide.rst docs/devguide.rst"
for path in $DOCS; do
  echo "linting $path"
  proselint $path
done
