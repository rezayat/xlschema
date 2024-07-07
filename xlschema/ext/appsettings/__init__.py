"""
appsettings
===========

Sometimes you want to read a setting from the command line.  Sometimes you want
to read it from an environment variable.  Sometimes you want to read it from a
config file.

And in some very special times, you want to allow the value to be passed using
some combination of the three.

The appsettings module provides an argparse subclass that allows pulling
settings from the command line, environment variables, or a yaml config file.

If the same value is provided in several of those locations, then env var
always beats config file, and command line always beats everything.

Usage is exactly the same as argparse, with the addition of some new kwargs on
initializing the parser and adding arguments to it.  Example::

    from appsettings import SettingsParser

    f = open('some_config_file.yaml')
    parser  = SettingsParser(yaml_file=f)

    parser.add_argument('--color', default='blue', env_var='FAVCOLOR')

    args = parser.parse_args()

    print args.color
    # If you've set the FAVCOLOR environment variable you should now see its
    # value printed to the console.  Otherwise you'd see 'blue'


Things to Know
==============

Options Only
------------

Only long form arguments like "--color" will provide env var and config file
fallbacks.  Positional arguments and short options like "-c" will behave just
like they do in the argparse module.

APP_SETTINGS_YAML
-----------------

If you don't provide a yaml_file argument to the SettingsParser constructor,
and the APP_SETTINGS_YAML environment variable is set, then that file will be
read and parsed to provide settings.  (Though they'll still be overridable by
environment variables and command line options.)

YAML File Format
----------------
The config file should be set up as below::

    color: 'blue'
    timeout: 10
    foo_bar: True

which can be overridden by running ``my_app.py --color blue --timeout 10 --foo-bar``. In this example, the argument ``--foo-bar`` uses argparse "store_true" action.

see: https://bitbucket.org/btubbs/appsettings
"""
from .parser import SettingsParser
