import argparse

import pytest

from xlschema.common.dict import Objdict, easy_options

URI = 'ok.txt'

class App:
    def __init__(self, uri, options=None, **kwds):
        self.uri = uri
        self.options = easy_options(options, kwds)

def test_options_none_kwds():
    app = App(URI, clean=True)
    assert app.options.clean

def test_options_objdict_kwds():
    options = Objdict(x=10)
    app = App(URI, options, clean=True)
    assert app.options.clean
    assert app.options.x == 10

def test_options_dict_kwds():
    options = dict(x=10)
    app = App(URI, options, clean=True)
    assert app.options.clean
    assert app.options.x == 10

def test_options_argparse_ns_kwds():
    options = argparse.Namespace(x=10)
    app = App(URI, options, clean=True)
    assert app.options.clean
    assert app.options.x == 10

def test_options_typeexception():
    options = range(10)
    with pytest.raises(TypeError):
        app = App(URI, options, clean=True)
