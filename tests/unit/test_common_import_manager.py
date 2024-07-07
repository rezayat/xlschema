import pytest
from xlschema.common.import_manager import ImportManager, ImportManagerError

LIBRARY = {
    'excel': ['ExcelWriter'],
    'doc': ['RstSchemaWriter'],
    'haskell': [
        'HaskellSchemaWriter',
        'HaskellModelWriter',
        'HaskellPersistWriter',
    ],
    'java': [
        'JavaWriter',
        'ScalaWriter',
    ],
    'python': [
        'PsycopgWriter',
        'SqlAlchemyWriter',
        'RecordsWriter',
        'PandasWriter',
    ],
    'django': [
        'DjangoAdminWriter',
        'DjangoModelsWriter',
        # 'DjangoAppWriter',
        'DjangoFactoriesWriter',
        'DjangoFactoryTestsWriter',
        'DjangoSerializerWriter',
        'DjangoRestViewsWriter',
    ],
    'sql': [
        'PostgresWriter',
        'PostgresMultiWriter',
        'PgEnumWriter',
        'PgTapWriter',
        'SqliteWriter',
    ],
    'sap': [
        'AbapWriter',
    ],
    'rlang': [
        'RlangWriter',
        'RMarkdownWriter',
    ],
    'yaml': ['YamlWriter'],
    'csv': ['CsvWriter'],
}


CLASS_INDEX = {
    'abap/oo': 'sap.AbapWriter',
    'csv/multi': 'csv.CsvWriter',
    'hs/model': 'haskell.HaskellModelWriter',
    'hs/persist': 'haskell.HaskellPersistWriter',
    'hs/schema': 'haskell.HaskellSchemaWriter',
    'java/hibernate': 'java.JavaWriter',
    'py/djadmin': 'python.DjangoAdminWriter',
    'py/django': 'python.DjangoAppWriter',
    'py/djfactories': 'python.DjangoFactoriesWriter',
    'py/djfactorytests': 'python.DjangoFactoryTestsWriter',
    'py/djmodels': 'python.DjangoModelsWriter',
    'py/djrestviews': 'python.DjangoRestViewsWriter',
    'py/djserializers': 'python.DjangoSerializerWriter',
    'py/pandas': 'python.PandasWriter',
    'py/psycopg': 'python.PsycopgWriter',
    'py/records': 'python.RecordsWriter',
    'py/sqlalchemy': 'python.SqlAlchemyWriter',
    'r/data': 'rlang.RlangWriter',
    'rmd/rmarkdown': 'rlang.RMarkdownWriter',
    'rst/sphinx': 'doc.RstSchemaWriter',
    'scala/hibernate': 'java.ScalaWriter',
    'sql/pgenum': 'sql.PgEnumWriter',
    'sql/pgschema': 'sql.PostgresMultiWriter',
    'sql/pgtap': 'sql.PgTapWriter',
    'sql/postgres': 'sql.PostgresWriter',
    'sql/sqlite': 'sql.SqliteWriter',
    'xlsx/validation': 'excel.ExcelWriter',
    'yml/yaml': 'yaml.YamlWriter',
}


class WriterImportManager(ImportManager):
    """Specialized Writer imports."""
    # context = __name__
    context = 'xlschema.writers'

    def gen_key(self, cls):
        return '{}/{}'.format(cls.file_suffix, cls.method)

def test_writer_import_manager_library():
    """produces both classes and class_index"""
    from xlschema.writers import SqliteWriter
    mgr = WriterImportManager(library=LIBRARY)
    class_index = mgr.class_index
    classes = mgr.classes
    assert class_index['sql/sqlite'] == 'sql.SqliteWriter'
    assert classes['sql/sqlite'] == SqliteWriter

def test_writer_import_manager_class_index():
    """produces only class_index"""
    from xlschema.writers import SqliteWriter
    mgr = WriterImportManager(class_index=CLASS_INDEX)
    assert not mgr.classes
    assert mgr.get_class('sql/sqlite') == SqliteWriter

def test_writer_import_manager_error():
    """neither library nor class_index are provided"""
    with pytest.raises(ImportManagerError):
        mgr = WriterImportManager()
