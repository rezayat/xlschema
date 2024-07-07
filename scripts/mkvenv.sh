source scripts/common.sh

section ">>> creating and activating virtualenv 'venv'"
virtualenv -p python3 venv
source venv/bin/activate

section ">>> installing requirements"
pip install -r requirements.txt

section ">>> install xlschema"
python setup.py develop

section ">>> DONE"
