"""General dictionary classes."""
import argparse


class Objdict(dict):
    """Dictionary with attribute access.

    >>> d = Objdict({'a':1})
    >>> d.a
    1
    >>> d.b = 10
    >>> d.b
    10
    >>> del d.b
    >>> d
    {'a': 1}
    >>> d.c
    Traceback (most recent call last):
    ...
    AttributeError: No such attribute: c
    >>> del d.c
    Traceback (most recent call last):
    ...
    AttributeError: No such attribute: c
    """

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)


def easy_options(options, kwds: dict) -> Objdict:
    """Returns dict as an Objdict instance.

    ..note:: Since this exposes ``dict`` attributes, be careful
             in using keys like ``update`` which will cause
             difficulties as it collides with the ``dict.update``
             method.

    Example::

        >>> class App:
        ...    def __init__(self, uri, options=None, **kwds):
        ...        self.uri = uri
        ...        self.options = easy_options(options, kwds)
        ...

        >>> app = App(None, clean=True)
        >>> app.options.clean
        True

        >>> options = dict(x=10)
        >>> app = App(None, options, clean=True)
        >>> app.options.clean
        True
        >>> app.options.x
        10
    """
    if options:
        if isinstance(options, Objdict):
            pass
        elif isinstance(options, dict):
            options = Objdict(options)
        elif hasattr(options, '__dict__'):
            options = Objdict(vars(options))
        else:
            raise TypeError("options type not recognized")
    else:
        options = Objdict()

    # Set default values for common options used by templates
    defaults = {
        'models_only': False,
        'clean': False,
        'update_only': False,
        'run': False,
        'populate': False,
        'view': False
    }

    # Apply defaults first, then user-provided options
    for key, default_value in defaults.items():
        if not hasattr(options, key) or getattr(options, key) is None:
            setattr(options, key, default_value)

    options.update(kwds)
    return options


def normalize_options(options=None, use_objdict=False):
    """Normalize options into a dict."""
    if options:
        if isinstance(options, dict):
            if use_objdict:
                return Objdict(options)
            return options
        elif isinstance(options, argparse.Namespace):
            if use_objdict:
                return Objdict(vars(options))
            return vars(options)
        else:
            raise TypeError('Must be an argparse.Namespace or a dict-like type.')
    else:
        return Objdict() if use_objdict else {}
