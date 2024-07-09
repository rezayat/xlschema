# flake8: noqa
"""A package containing xlschema.Writer classes.

Writers consume models and enum instances and apply
:py:mod:`xlschema.Field` instances to render code from templates.

It is the principle method of extending ``xlschema``::

    SchemaWriter
        ExcelWriter
        TemplateWriter
            HaskellWriter
                HaskellSchemaWriter
                HaskellSchemaWriter
                HaskellPersistWriter
            JavaWriter
            ScalaWriter
            PythonWriter
                PsycopgWriter
                DjangoWriter
                    DjangoModelsWriter
                    DjangoAdminWriter
                    DjangoTestsWriter
                    DjangoFactoriesWriter
                    DjangoFactoryTestsWriter
                    DjangoSerializerWriter
                SqlAlchemyWriter
                RecordsWriter
                PandasWriter
                FactoryWriter
            SqlWriter
                PostgresWriter
                    PsycopgWriter
                    PgEnumWriter
                    PgTapWriter
                SqliteWriter
            RstWriter
            RMarkdownWriter
            AbapWriter
            YamlWriter
            CsvWriter
"""

# ----------------------------------------------------------
# WRITERS
# ----------------------------------------------------------
from .excel import ExcelWriter

from .doc import RstSchemaWriter

from .haskell import (
    HaskellSchemaWriter,
    HaskellModelWriter,
    HaskellPersistWriter,
)

from .java import JavaWriter, ScalaWriter

from .python import (
    PsycopgWriter,
    SqlAlchemyWriter,
    RecordsWriter,
    PandasWriter,
)

from .django import (
    DjangoAdminWriter,
    DjangoModelsWriter,
    # DjangoAppWriter,
    DjangoFactoriesWriter,
    DjangoFactoryTestsWriter,
    DjangoSerializerWriter,
    DjangoRestViewsWriter,
)

from .sql import (
    PostgresWriter,
    PostgresMultiWriter,
    PgEnumWriter,
    PgTapWriter,
    SqliteWriter
)

from .sap import AbapWriter

from .rlang import RlangWriter, RMarkdownWriter

from .yaml import YamlWriter

from .csv import CsvWriter
