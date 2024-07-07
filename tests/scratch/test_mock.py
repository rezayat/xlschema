import os
import pytest

def rm(fname):
    os.remove(fname)


def test_mock_in_pytest(mocker):

    # mocker.Mock()
    m = mocker.Mock()
    m.name.return_value = 100
    assert m.name() == 100

    # side_effect
    m.error.side_effect = ValueError('A custom value error')
    with pytest.raises(ValueError):
        m.error()

    # mocker.patch()
    mocker.patch('os.remove')
    rm('file')
    os.remove.assert_called_once_with('file')
