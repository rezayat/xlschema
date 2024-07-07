# """

# This test requires:

# - docker::

#     docker pull postgres:alpine

# - python packages::

#     pip install dockerctx

# """
# import argparse
# import os
# import time

# import psycopg2
# import pytest
# from dockerctx import new_container

# import xlschema

# # skip all tests in this file (comment out to activate)
# pytestmark = pytest.mark.skip()



# # UTILITIES
# # ----------------------------------------------------------------------

# OUTPUT = 'data/output'

# def xlschema_postgres_from_file(path):
#     # using sqlite syntax (which is valid postgres syntax)
#     # because psycopg2 doesn't read COPY
#     generated = 'schema_sqlite.sql'
#     options = argparse.Namespace(output=OUTPUT, clean=False)
#     xlschema.XLSchema(uri=path, options=options).write('sql/sqlite')
#     # read generated sql
#     sqlfile = os.path.join(OUTPUT, generated)
#     with open(sqlfile) as f:
#         sql = f.read()
#     con = psycopg2.connect("host=localhost dbname=postgres user=postgres")
#     cur = con.cursor()
#     cur.execute(sql)
#     cur.execute("select name from person where id=1")
#     name = cur.fetchone()[0]
#     assert name=="jon"
#     cur.close()
#     con.close()


# # FIXTURES
# # ----------------------------------------------------------------------
# @pytest.fixture(scope='function')
# def db():
#     with new_container(
#             image_name='postgres:alpine',
#             ports={5432: 5432},
#             ready_test=lambda: time.sleep(3) or True) as container:
#         yield container

# # TESTS
# # ----------------------------------------------------------------------
# def test_xlschema_xlsx_postgres(db):
#     xlschema_postgres_from_file('data/xlsx/schema.xlsx')

# def test_xlschema_yaml_postgres(db):
#     xlschema_postgres_from_file('data/yml/schema.yml')
