import argparse
import os

import pytest

import xlschema

# HELPERS
# ----------------------------------------------------------------------
join = os.path.join
cmd = lambda xs: " ".join(xs)

# CONSTANTS
# ----------------------------------------------------------------------
METHODS = [
    'abap/oo',
    'csv/multi',
    'hs/model',
    'hs/persist',
    'hs/schema',
    'py/djadmin',
    'py/django',
    'py/djfactories',
    'py/djmodels',
    'py/djserializers',
    'py/dummy',
    'py/pandas',
    'py/psycopg',
    'py/records',
    'py/sqlalchemy',
    'r/data',
    'rmd/rmarkdown',
    'rst/sphinx',
    'sql/pgenum',
    'sql/pgschema',
    'sql/pgtap',
    'sql/postgres',
    'sql/sqlite',
    'xlsx/validation',
    'yml/yaml',
]

METHODS_PROPS = [
    'scala/hibernate',
    'java/hibernate',
    'py/djfactorytests',
    'py/djrestviews',
    'scala/hibernate',
]

ROOT = 'tests/data'

DB_DIR = join(ROOT, 'db')
FIXTURES = join(ROOT, 'fixtures')
LOGS_DIR = join(ROOT, 'logs')

TEMPLATES_DIR = join(ROOT, 'templates')

OUTPUT = join(ROOT, 'output')
SPEC_DIR = join(ROOT, 'spec')
XL_DIR = join(ROOT, 'xlsx')
YL_DIR = join(ROOT, 'yml')

SPLIT_IN_DIR = join(XL_DIR, 'to_split')
SPLIT_OUT_DIR = join(OUTPUT, 'splits')

SCHEMA_DIR = join(OUTPUT, 'schema')

# Shell commands
XLSCHEMA = 'python3 -m xlschema'
XLSCHEMA_OUT = cmd([XLSCHEMA, '--output', OUTPUT])
FROM_URI = cmd([XLSCHEMA_OUT, 'from_uri'])

# path commands
spec = lambda name: join(SPEC_DIR, name+'.yml')
xlsx = lambda name: join(XL_DIR, name+'.xlsx')
yaml = lambda name: join(YL_DIR, name+'.yml')
sqldb = lambda name: join('sqlite:///', DB_DIR, name+'.sqlite')
split_in = lambda name: join(SPLIT_IN_DIR, name+'.xlsx')
split_out = lambda name: join(SPLIT_OUT_DIR, name+'.xlsx')
dual = lambda name: [xlsx(name), yaml(name)]

to_output = lambda path: join(OUTPUT, path)

SCHEMA_XLSX, SCHEMA_YAML = dual('schema')
DJANGO_XLSX, DJANGO_YAML = dual('django')
M2M_XLSX, M2M_YAML = dual('manytomany')
SPLIT_XLSX = split_in('test-splitter')
SPEC_YAML = spec('test')

CONFIG_YAML = join(ROOT, 'config.yml')
TEMPLATE_XLSX = join(ROOT, 'empty.xltx')

SKIP_ERROR_FILES = [
    'README.md',
    'node_error.yml',
    'node_malformed.yml']

XL_ERROR_FILES = [
    'test-error-missing-type.xlsx',
    'test-error-unreadable-format.xlsx',
    'test-error-no-data-empty.xlsx',
]

XL_PARTIAL_FILES = [
    'test-partial-no-enums.xlsx',
]

XL_SKIP_FILES = XL_ERROR_FILES + XL_PARTIAL_FILES

XL_FILES = [join(XL_DIR, f) for f in os.listdir(XL_DIR)
            if f.endswith('.xlsx') and f not in XL_SKIP_FILES]

TEST_DB = sqldb('test')
POSTGRES_DB = 'postgresql://sa:sa@localhost:5432/db'

# options

def nspace(options, **kwds):
    """NOTE: If dikt is not copied, namespace bleeds into unrelated tests."""
    if isinstance(options, dict):
        dict_copy = options.copy()
    elif isinstance(options, argparse.Namespace):
        dict_copy = vars(options).copy()
    else:
        raise TypeError("options must be dict or argparse.Namespace")
    dict_copy.update(kwds)
    return argparse.Namespace(**dict_copy)

OPTIONS_BASE = dict(
    output=OUTPUT,
    clean=False, update_only=False,
    models_only=False,
)

OPTIONS_DEFAULT = nspace(OPTIONS_BASE)

OPTIONS_DEFAULT_MAKO = nspace(OPTIONS_BASE)

OPTIONS_TABLE = nspace(OPTIONS_BASE,
    sql=None,
    table=['person', 'vehicle', 'person_vehicle'])

OPTIONS_SQL = nspace(OPTIONS_BASE,
    table=[],
    sql=['select * from person', 'select * from vehicle'])

sql = lambda statement: nspace(OPTIONS_BASE, table=[], sql=[statement])

# UTILITIES
# ----------------------------------------------------------------------
shell = lambda xs: os.system(" ".join(xs))

def cleanup():
    os.system('rm -rf {}/*'.format(OUTPUT))

def clean_local_dir():
    os.system('rm -r ./.xlschema')

def exists(target):
    target = join(OUTPUT, target)
    return all([
        os.path.exists(target),
        os.stat(target).st_size > 0
    ])

def dir_exists(target):
    target = join(OUTPUT, target)
    return all([
        os.path.exists(target),
    ])

def check(target):
    assert exists(target)
    os.remove(join(OUTPUT, target))

def check_template(rendered_path, expected):
    assert exists(rendered_path)
    path = os.path.join(OUTPUT, rendered_path)
    with open(path) as f:
        content = f.read()
    return content == expected

def get_app(fname, options=None, **kwds):
    if not options and kwds:
        options = argparse.Namespace(**kwds)
    elif options and kwds:
        options = nspace(options, **kwds)
    elif options and not kwds:
        options = options
    else:
        options = OPTIONS_DEFAULT
    if fname.endswith('.xlsx'):
        path = join(XL_DIR, fname)
    elif fname.endswith('.yml'):
        path = join(YL_DIR, fname)
    else:
        path = fname
        # raise Exception('extension not supported')
    return xlschema.XLSchema(uri=path, options=options)

def app_check(fname, method, options=None, **kwds):
    app = get_app(fname, options, **kwds)
    fileout = fname + '.out'
    output = to_output(fileout)
    app.write(method, to_path=output)
    check(fileout)

# FIXTURES
# ----------------------------------------------------------------------

@pytest.fixture(scope="module")
def populate_db():
    shell(['sqlite3', join(DB_DIR, 'test.sqlite'), '<', join(FIXTURES,'test.sql')])


@pytest.fixture(scope="module", params=[SCHEMA_XLSX, SCHEMA_YAML])
def app(request):
    app = xlschema.XLSchema(uri=request.param, options=OPTIONS_DEFAULT)
    yield app # provide the fixture value
    cleanup()

@pytest.fixture(scope="module", params=[DJANGO_XLSX, DJANGO_YAML])
def prop_app(request):
    app = xlschema.XLSchema(uri=request.param, options=OPTIONS_DEFAULT)
    yield app # provide the fixture value
    cleanup()

@pytest.fixture(scope="module", params=[M2M_XLSX, M2M_YAML])
def m2mapp(request):
    app = xlschema.XLSchema(uri=request.param, options=OPTIONS_DEFAULT)
    yield app # provide the fixture value
    cleanup()

@pytest.fixture(scope="module", params=XL_FILES)
def xlapp(request):
    app = xlschema.XLSchema(uri=request.param, options=OPTIONS_DEFAULT)
    yield app # provide the fixture value
    cleanup()

@pytest.fixture(scope="module", params=[TEST_DB])
def dbapp(request):
    app = xlschema.XLSchema(uri=request.param, options=OPTIONS_TABLE)
    yield app # provide the fixture value
    cleanup()

@pytest.fixture(scope="module", params=[TEST_DB])
def sqlapp(request):
    app = xlschema.XLSchema(uri=request.param, options=OPTIONS_SQL)
    yield app # provide the fixture value
    cleanup()

@pytest.fixture(scope="module", params=[OPTIONS_DEFAULT,
                                        OPTIONS_DEFAULT_MAKO])
def tmplapp(request):
    app = get_app('node.yml', options=request.param)
    yield app
    cleanup()

# @pytest.fixture(autouse=True)
# def add_np(doctest_namespace):
#     doctest_namespace['xlschema'] = xlschema
#     doctest_namespace['argparse'] = argparse
