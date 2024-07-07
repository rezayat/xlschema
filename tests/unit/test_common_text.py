from hypothesis import given
from hypothesis.strategies import text

from xlschema.common.text import Text


@given(text())
def test_clean(s):
    result = Text(s).clean()
    assert any(not i in result for i in Text.WHITELIST)

# @given(text())
# def test_quote(s):
#     result = Text(s).quote
#     assert result.unquote == s

def test_quote():

    pairs = [
        ('"', ''),
        ("'", ''),
        ('hello"', '"hello"'),
        ("he's", '"he\'s"'),
    ]
    for x,y in pairs:
        assert Text(x).quote == y

def test_timestamp():
    t = Text.timestamp()
    assert not t is None

def test_plural():
    assert Text('boy').plural() == 'boys'
    assert Text('sash').plural() == 'sashes'
    assert Text('box').plural() == 'boxes'
