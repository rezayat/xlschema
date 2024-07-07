git checkout -b xlschema2.7 v1.0-py2.7
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python setup.py develop
echo "DONE"
