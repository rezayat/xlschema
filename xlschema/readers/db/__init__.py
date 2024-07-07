"""DB to Model SchemaReader."""
from datetime import date, datetime
from collections import OrderedDict

from .. import abstract
from ... import models

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker


# ----------------------------------------------------------
# DB Conversion
# ----------------------------------------------------------


class DBToModel(abstract.SchemaReader):
    """Parses db tables into relational models."""

    def preprocess(self):
        """Runs before main process method for conversion.

        Place reader specific instance variable here
        """
        self.engine = create_engine(self.uri)
        self.meta = MetaData()
        self.meta.reflect(bind=self.engine)

    def process(self):
        """Main process for conversion."""
        self.log.debug("processing %s", self.uri)

        tableitems = list(self.meta.tables.items())
        model_names = []

        for name, table in tableitems:
            if self.options.table:
                if name not in self.options.table:
                    continue
            model_names.append(name)
            model = models.Model(name)
            for col in table.columns:
                field = dict(name=col.name, type=col.type.python_type.__name__)
                if col.primary_key:
                    field['index'] = 'pk'
                if col.foreign_keys:
                    field['index'] = 'fk'
                if not col.nullable:
                    field['required'] = True
                if col.default:
                    field['default'] = col.default  # pragma: no cover
                model.fields.append(self.field_class.from_dict(field))

            rows = self.engine.execute(table.select())
            for row in rows:
                cleaned_row = model.row_clean(row)
                model.data.append(cleaned_row)
            self.schema.models.append(model)

        self.post_process(model_names)


class SqlToModel(abstract.SchemaReader):
    """Sql to abstract models reader."""

    def preprocess(self):
        """Preparations and setup before main process."""
        self.name = 'query'
        self.engine = create_engine(self.uri)
        self.meta = MetaData()
        self.meta.reflect(bind=self.engine)
        self.session_factory = sessionmaker(bind=self.engine)

    def populate(self, counter, sql, rows):
        """Populate main models from sql statement and its query results.

        :param counter: counts no of sql statements
        :type counter: int

        :param sql: current sql statement
        :type sql: str

        :param rows: result of sql query
        :type rows: :py:class:`sqlalchemy.ResultProxy`
        """
        fieldnames = rows.keys()
        print('fieldnames: ', fieldnames)
        _rows = [row for row in rows]
        print("rows:",_rows)
        types = self.get_types(_rows[0], fieldnames)
        indexes = self.get_indexes(fieldnames)
        fields = [
            dict(name=f, type=t, index=i)
            for f, t, i in zip(fieldnames, types, indexes)
        ]
        self.schema.models.append(
            models.Model(
                name='{}{}'.format(self.name, counter),
                fields=[self.field_class.from_dict(f) for f in fields],
                properties=OrderedDict([('sql', sql)]),
                data=_rows,
            )
        )

    def process(self):
        """Main process to execute sql into models."""
        for i, sql in enumerate(self.options.sql):
            self.log.debug('executing: %s', sql)
            try:
                session = self.session_factory()
                print('sql:', sql)
                rows = session.execute(sql)
                self.populate(i, sql, rows)
                session.commit()
            except:  # noqa: E722
                session.rollback()
                raise
            finally:
                session.close()

        model_names = [model.name for model in self.schema.models]
        self.log.debug('model_names: %s', model_names)
        self.post_process(model_names)

    @staticmethod
    def get_types(row, fieldnames):
        """Retrieve types for a given concrete row."""
        def _get_type(val):
            types = {
                'int': int,
                'str': str,
                'float': float,
                'date': date,
                'datetime': datetime,
            }
            for label, type_ in types.items():
                if isinstance(val, type_):
                    return label

        _types = tuple(_get_type(i) for i in row)
        _result = []
        for name, type_ in zip(fieldnames, _types):
            if 'date' in name:
                _result.append('date')
            else:
                _result.append(type_)
        return _result

    @staticmethod
    def get_indexes(fields):
        """Retrieve indexes from fields."""
        def _get_index(field):
            if field in ['id']:
                return 'pk'
            if field.endswith('_id'):
                return 'fk'
            return

        return tuple(_get_index(f) for f in fields)
