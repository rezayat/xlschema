#!/usr/bin/env python3
"""xlschema is a round-trip relational model code generation tool.

xlschema enables a developer or datamodel author to design and populate
relational tables in microsoft xl or yaml and automatically convert to postgresql,
sqlite, django, sqlalchemy, and haskell code::

    usage: xlschema from_uri [-h] [--format FORMAT] [--run] [--populate]
                             [--update-only] [--schema-only]
                             [--table [TABLE [TABLE ...]]] [--sql [SQL [SQL ...]]]
                             [--prefix PREFIX] [--view]
                             uri

    positional arguments:
      uri                   uri to operate on

    optional arguments:
      -h, --help            show this help message and exit
      --format FORMAT, -f FORMAT
                            abap/oo, hs/model, hs/persist, hs/schema,
                            java/hibernate, py/djadmin, py/django, py/djfactories,
                            py/djfactorytests, py/djmodels, py/djrestviews,
                            py/djserializers, py/pandas, py/psycopg, py/records,
                            py/sqlalchemy, r/data, rmd/rmarkdown, rst/sphinx,
                            scala/hibernate, sql/pgenum, sql/pgschema, sql/pgtap,
                            sql/postgres, sql/sqlite, xlsx/validation, yml/yaml
      --run, -r             autorun with all options
      --populate, -p        populate database
      --update-only, -u     only gen update code
      --schema-only         only gen schema code
      --table [TABLE [TABLE ...]], -t [TABLE [TABLE ...]]
                            table(s) to dump
      --sql [SQL [SQL ...]], -s [SQL [SQL ...]]
                            sql to use for selection
      --prefix PREFIX       set prefix of output
      --view, -v            include views
"""

# from .config import Config
import os
from .plugins.cmdline import PluginApplication

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------

CONFIG_YML = '.xlschema.yml'
HOME = os.environ['HOME']
PKGDIR = os.path.dirname(__file__)

# ----------------------------------------------------------
# Commandline Application
# ----------------------------------------------------------

class Application(PluginApplication):
    """XLSchema: Convert from XLSX/YAML to sql/django/sqlalchemy/haskell models."""

    name = 'xlschema'
    description = 'Round-trip relational model code generation framework.'
    epilog = ''
    version = '0.3.16'
    default_args = ['--help']
    config_yml = (CONFIG_YML if os.path.exists(CONFIG_YML) else
                 os.path.join(PKGDIR, CONFIG_YML))

    def set_general_options(self):
        """Set general or application-wide options."""
        option = self.parser.add_argument
        option('--output', '-o', type=str, default='output', help='set output directory')
        option('--prefix', type=str, help="set prefix of output")
        option('--clean', '-c', action='store_true', help='clean output dir before generation')


if __name__ == '__main__':
    Application().cmdline()
