import pytest

from conftest import (
    METHODS,
    exists, get_app, cleanup, check)
from xlschema.config import register
from xlschema.writers.excel import ExcelWriter


@register
class ExcelWriterMax(ExcelWriter):
    """Specialized version ExcelWriter with max column width."""

    file_suffix = 'xlsx'
    method = 'max'
    XL_COLUMN_WIDTH_METHOD = 'max'

@register
class ExcelWriterMedian(ExcelWriter):
    """Specialized version ExcelWriter with median column width."""

    file_suffix = 'xlsx'
    method = 'median'
    XL_COLUMN_WIDTH_METHOD = 'median'

@register
class ExcelWriterInt(ExcelWriter):
    """Specialized version ExcelWriter with custom integer column width."""

    file_suffix = 'xlsx'
    method = 'int'
    XL_COLUMN_WIDTH_METHOD = 20

@register
class ExcelWriterLength(ExcelWriter):
    """Specialized version ExcelWriter with field length column width."""

    file_suffix = 'xlsx'
    method = 'validation'
    XL_COLUMN_WIDTH_METHOD = None

# TESTS
# ----------------------------------------------------------------------
def test_excel_writer_schema(app):
    # app.write('sql/sqlite')
    app.write(*METHODS)
    generated = 'schema_sqlite.sql'
    assert exists(generated)

def test_excel_writer_types():
    app = get_app('test-types.xlsx')
    app.write('xlsx/validation')
    generated = 'test-types_validation.xlsx'
    check(generated)

def test_excel_writer_no_type_error():
    from xlschema.fields.abstract import FieldError
    with pytest.raises(FieldError):
        app = get_app('test-error-missing-type.xlsx')

def test_excel_writer_no_enum():
    app = get_app('test-partial-no-enums.xlsx')
    with pytest.raises(AssertionError):
        app.write('xlsx/validation')
    #generated = 'test-no-enums_validation.xlsx'
    #check(generated)
