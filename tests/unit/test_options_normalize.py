import argparse
import hashlib
import os

import pytest

import xlschema
from xlschema.common.dict import Objdict, normalize_options

from conftest import OPTIONS_DEFAULT, OUTPUT, METHODS, yaml


OPTIONS_NSPACE = argparse.Namespace(output=OUTPUT)
OPTIONS_DICT   = dict(output=OUTPUT)
OPTIONS_OBDICT = Objdict(dict(output=OUTPUT))
OPTIONS_EMPTY  = None
OPTIONS_ERROR  = [1,2,3]

OPTIONS_CASES = [OPTIONS_NSPACE,
                 OPTIONS_DICT,
                 OPTIONS_OBDICT,
                 OPTIONS_EMPTY,
                 OPTIONS_ERROR]

OPTIONS = vars(OPTIONS_DEFAULT)

@pytest.fixture(scope="function", params=OPTIONS_CASES)
def options(request):
    yield request.param # provide the fixture value

def test_options_to_dict(options):
    try:
        options = normalize_options(options)
        assert isinstance(options, dict)
        if options:
            assert 'output' in options
        else:
            with pytest.raises(AttributeError):
                output = options.output
    except TypeError as exc:
        pass


def test_options_to_objdict(options):
    try:
        options = normalize_options(options, use_objdict=True)
        assert isinstance(options, Objdict)
        if options:
            assert options.output
        else:
            with pytest.raises(AttributeError):
                output = options.output
    except TypeError as exc:
        pass

def files_hashes_from_app(options):
    _hashes = []
    _files = []
    in_file = yaml('node')
    app = xlschema.XLSchema(in_file, options)
    app.write(*METHODS)
    for fname in os.listdir(OUTPUT):
        path = os.path.join(OUTPUT, fname)
        if os.path.isfile(path):
            with open(path, 'rb') as f:
                content = f.read()
                md5 = hashlib.md5(content).hexdigest()
                _files.append(path)
                _hashes.append(md5)
    return (_files, _hashes)

def test_namespace_objdict_equivalence():
    options_ns = argparse.Namespace(**OPTIONS)
    options_et = normalize_options(OPTIONS, use_objdict=True)

    files_ns, hashes_ns = files_hashes_from_app(options_ns)
    files_et, hashes_et = files_hashes_from_app(options_et)

    for f, ns, et in zip(files_ns, hashes_ns, hashes_et):
        if f.endswith('.xlsx'): # excel files are unpredictable
            continue
        # print(f, ns, et)
        assert ns == et, "{} is different".format(f)
