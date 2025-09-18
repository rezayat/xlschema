import pytest

from xlschema.fields.abstract import FieldError

from conftest import get_app, check

def test_spreadsheets(xlapp):
    assert len(xlapp.schema.models) > 0
    assert len(xlapp.schema.enums)  > 0
    assert len(xlapp.schema.types)  > 0

def test_empty_xlsx():
    app = get_app('test-empty.xlsx')
    app.write('sql/sqlite')
    check('test-empty_sqlite.sql')

def test_error_unreadable_format_xlsx():
    from xlschema.common.exceptions import SchemaParsingError
    with pytest.raises(SchemaParsingError):
        app = get_app('test-error-unreadable-format.xlsx')

def test_error_missing_type_xlsx():
    with pytest.raises(FieldError):
        app = get_app('test-error-missing-type.xlsx')

def test_error_no_data_empty_xlsx():
    from xlschema.common.exceptions import SchemaParsingError
    with pytest.raises(SchemaParsingError):
        app = get_app('test-error-no-data-empty.xlsx')

def test_partial_no_enums_xlsx():
    app = get_app('test-partial-no-enums.xlsx')
    assert len(app.schema.models) > 0
    assert len(app.schema.enums) == 0
    assert len(app.schema.types) > 0
