import os
import sqlite3

from conftest import OUTPUT, check


# TESTS
# ----------------------------------------------------------------------
def test_validates_sql_sqlite(app):
    app.write('sql/sqlite')
    generated = 'schema_sqlite.sql'
    sqlfile = os.path.join(OUTPUT, generated)
    with open(sqlfile) as f:
        sql = f.read()
    check(generated)
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.executescript(sql)
    cursor.execute("select name from person where id=1")
    name = cursor.fetchone()[0]
    assert name=="jon"
    cursor.close()
    connection.close()
