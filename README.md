# xlschema: generate model code from xlsx/yaml files

**xlschema** is a python 3 tool and library which generates boilerplate code for relational database models from YAML files, MS Excel templates or directly from database connections.

## Quickstart

Installation

```
$ git clone https://github.com/rezayat/xlschema.git
$ cd xlschema
$ rye sync
$ source .venv/bin/activate
```

xlschema uses [rye](https://rye.astral.sh/guide/) as development tool.

View the [YAML](http://yaml.org) at `tests/data/yml/node.yml` using your preferred text editor:

```yaml
enums:
  - name: status
    data:
      - [created,  Created]
      - [open,     Open]
      - [finished, Finished]
      - [closed,   Closed]

models:
  - name: node
    fields:
      - name: id
        type: int
        index: pk

      - name: parent_id
        type: int
        index: fk

      - name: name
        type: str
        length: 50
        required: true

      - name: status
        type: str
        length: 10
        required: true
        constraint: enum

    data:
      - [1, null, A, created]
      - [2, 1,    B, open]
      - [3, 1,    C, finished]
      - [4, 2,    D, created]
      - [5, 4,    E, closed]
      - [6, 4,    F, finished]

```

Now with the virtualenv environment activated and from the root of the `xlschema` directory run the following:

```
$ python3 -m xlschema from_uri --format=sql/pgenum tests/data/yml/node.yml
```

You should see some log information about a file being generated. Now view the file, `node_pgenum.sql`, in `./tests/data/output`:

```sql

drop type status cascade;
create type status as enum (
    'created',
    'open',
    'finished',
    'closed'
);

drop table if exists node cascade;
create table node
(
    id integer primary key,
    parent_id integer references node (id),
    name varchar(50) not null,
    status status not null
);


-- node DATA
-- ---------------------------------------------------------------
COPY node (id, parent_id, name, status) FROM stdin;
1	\N	A	created
2	1	B	open
3	1	C	finished
4	2	D	created
5	4	E	closed
6	4	F	finished
\.

```

If you have `postgres`, you can test that this generated sql works by doing something similar to this (with the appropriate connection info):

```
$ psql -f node_pgenum.sql
```

Now, let's try another format, and run xlschema to generate a django models file:

```
$ python3 -m xlschema from_uri --format=py/djmodels tests/data/yml/node.yml
```

You should see a file called `node_djmodels.py` in the output directory:

```python
from datetime import datetime
from django.db import models

# NODE
# ----------------------------------------------------------
STATUS = [
    ("created", "Created"),
    ("open", "Open"),
    ("finished", "Finished"),
    ("closed", "Closed"),
]

class Node(models.Model):
    id = models.IntegerField(blank=False, null=False, primary_key=True)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="children", on_delete=models.CASCADE)
    name = models.CharField(blank=False, null=False, max_length=50)
    status = models.CharField(blank=False, null=False, choices=STATUS, max_length=10)
    class Meta:
        db_table = "node"
        verbose_name_plural = "nodes"

    def __str__(self):
        return "Node-{}".format(self.id)
```

## Commandline Usage

XLSchema is a built around a plugin framework. Its core features are applied by the `from_uri` subcommand, which converts from xlsx/yaml formats or a db_uri to the implemented xlschema target formats (django models.py, sqlalchemy models, sql files, etc..):

```
$ python3 -m xlschema --help
usage: xlschema [-h] [--output OUTPUT] [--prefix PREFIX] [--clean] plugin ...

Round-trip relational model code generation framework.

positional arguments:
  plugin
    from_uri            Generate model code from URI.
    echo                Echo command-line options.
    display             Display available writers.
    to_sqla             Generate sqlalchemy schemas from databases.
    split_xlsx          Splits xlsx sheets from a column.

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        set output directory (default: None)
  --prefix PREFIX       set prefix of output (default: None)
  --clean, -c           clean output dir before generation (default: False)

```

To see the available formats and other options in more detail::

```
$ python3 -m xlschema from_uri --help
usage: xlschema from_uri [-h] [--run] [--populate] [--update-only]
                         [--models-only] [--view]
                         [--table [TABLE [TABLE ...]]] [--sql [SQL [SQL ...]]]
                         [--format [FORMAT [FORMAT ...]]]
                         uri

positional arguments:
  uri                   uri to operate on

optional arguments:
  -h, --help            show this help message and exit
  --run, -r             autorun with all options
  --populate, -p        populate database
  --update-only, -u     only gen update code
  --models-only         only gen model code
  --view, -v            include views
  --table [TABLE [TABLE ...]], -t [TABLE [TABLE ...]]
                        table(s) to dump
  --sql [SQL [SQL ...]], -s [SQL [SQL ...]]
                        sql to use for selection
  --format [FORMAT [FORMAT ...]], -f [FORMAT [FORMAT ...]]
                        abap/oo, csv/multi, hs/model, hs/persist, hs/schema,
                        java/hibernate, py/djadmin, py/django, py/djfactories,
                        py/djfactorytests, py/djmodels, py/djrestviews,
                        py/djserializers, py/pandas, py/psycopg, py/records,
                        py/sqlalchemy, r/data, rmd/rmarkdown, rst/sphinx,
                        scala/hibernate, sql/pgenum, sql/pgschema, sql/pgtap,
                        sql/postgres, sql/sqlite, xlsx/validation, yml/yaml

```


Typical use cases would be as follows:


### From Files (YAML/XLSX)

- Dump schema and data from yaml specification file into all formats
```
$ python3 -m xlschema from_uri tests/data/yml/node.yml
```

- Dump schema and data from xlsx specification file into single format
```
$ python3 -m xlschema from_uri --format=sql/sqlite tests/data/xlsx/schema.xlsx
```


### From Database

- Dump all tables in db into all formats
```
$ python3 -m xlschema from_uri sqlite:///data/db/test.sqlite
```

- Dump all tables in db into single format
```
$ python3 -m xlschema from_uri sqlite:///data/db/test.sqlite --format=sql/sqlite
```

- Dump results of sql statements into all formats:
```
$ python3 -m xlschema from_uri sqlite:///data/db/test.sqlite --sql 'select * from person'
```

- Dump tables into all formats:
```
$ python3 -m xlschema from_uri sqlite:///data/db/test.sqlite --table person vehicle
```


## User Guide and API Documentation

- See the [userguide](docs/userguide.rst) and the [api](docs/api) if you would just like to use the project.

- See the [devguide](docs/devguide.rst) is you would like to contribute or help in the development of the project.
