import pathlib
import tempfile

from conftest import OUTPUT, SCHEMA_DIR, exists, cleanup
from xlschema.depends import DependencyManager


# TESTS
# ----------------------------------------------------------------------
def test_pgschema_depends(app):
    app.write('sql/pgschema')
    assert exists('schema/tables/person.sql')
    assert exists('schema/fixtures/person.sql')
    assert exists('schema/tables/vehicle.sql')
    assert exists('schema/fixtures/vehicle.sql')
    assert exists('schema/tables/person_vehicle.sql')
    assert exists('schema/fixtures/person_vehicle.sql')

    mgr = DependencyManager(SCHEMA_DIR)
    mgr.process()

    # print('pathmap: ', mgr.pathmap)
    # print('depmap:', mgr.depmap)
    # print('groups: ', mgr.groups)

    assert mgr.pathmap is not None
    assert mgr.depmap is not None
    assert mgr.groups is not None
    cleanup()

def test_fake_depends():
    with tempfile.TemporaryDirectory() as tmpdir:
        f1 = pathlib.Path(tempfile.mktemp(suffix='.sql', dir=tmpdir))
        f2 = pathlib.Path(tempfile.mktemp(suffix='.foo', dir=tmpdir))
        for f in [f1, f2]:
            f.touch()
            assert f.is_file()
        mgr = DependencyManager(tmpdir)
        mgr.load_dir(tmpdir)
