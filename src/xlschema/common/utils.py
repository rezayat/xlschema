"""Common utility functions and classes."""
from pathlib import Path


def dictmerge(*dicts, **kwds):
    """Merge a list of dictionary and update merged with kwds.

    :param dicts: list of dictionaries to be merged sequentially
    :type dicts: List[dict]

    :param kwds: optional keyword args to be merged at the end
    :type kwds: dict

    ..note:: The order of priority is given to the last dicts and finally
             the kwds.

    Usage::

        >>> d1 = dict(a=1)
        >>> d2 = dict(b=2)
        >>> d3 = dict(b=3, c=4)
        >>> res = dictmerge(d1, d2, d3, a=2)
        >>> list(sorted(res.items()))
        [('a', 2), ('b', 3), ('c', 4)]

        >>> dictmerge(a=1)
        {'a': 1}

        >>> res = dictmerge(d1, b=2)
        >>> list(sorted(res.items()))
        [('a', 1), ('b', 2)]

    """
    _origin = {}
    for _dict in dicts:
        _origin.update(_dict)
    _origin.update(kwds)
    return _origin


def is_number(obj):
    """Checks if obj is an int or a float or a long.

    >>> is_number(10)
    True
    """
    return isinstance(obj, (int, float))


def is_xlsx(path: str) -> bool:
    """Returns True if path is an ``*.xlsx`` file.

    :param path: a path to a file
    :returns: boolean value

    >>> p = Path('/tmp/hello.xlsx')
    >>> p.touch()
    >>> is_xlsx('/tmp/hello.xlsx')
    True
    >>> p.unlink()
    """
    return all([
        Path(path).is_file(),
        path.endswith('.xlsx')
    ])


def is_yaml(path: str) -> bool:
    """Returns True if path is a ``*.yaml`` or ``*.yml`` file.

    :param path: a path to a file
    :returns: boolean value

    >>> p = Path('/tmp/hello.yaml')
    >>> p.touch()
    >>> is_yaml('/tmp/hello.yaml')
    True
    >>> p.unlink()
    """
    return all([
        Path(path).is_file(),
        any(path.endswith(i) for i in ['.yml', '.yaml'])
    ])
