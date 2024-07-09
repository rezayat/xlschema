import os
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Enum
from sqlalchemy import (Float, Integer, String, Text, Boolean,
                        Date, Time, Interval)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

DBI_URI = os.getenv('DBI_URI', '${data.config.DB_URI}')
# engine = create_engine('sqlite:///:memory:', echo=True)
# engine = create_engine('sqlite:///sqlite.db', echo=True)
engine = create_engine(DBI_URI, echo=False)


class DeclarativeBase(object):
    id =  Column(Integer, primary_key=True)

    def __repr__(self):
        return "<{} id={}>".format(
            self.__class__.__name__,
            self.id)

    @classmethod
    def from_dict(cls, dikt, **kwds):
        """Instanciate class from a dict
        """
        for key in cls.__dict__:
            if key == 'id' or key.startswith('_'):
                continue
            else:
                if dikt.has_key(key):
                    kwds[key] = dikt[key]
                else:
                    kwds[key] = None
        return cls(**kwds)




Base = declarative_base(cls=DeclarativeBase)
metadata = Base.metadata
metadata.bind = engine

# create session
Session = sessionmaker(bind=engine)

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def sql(self, sql_string, *args, **kwds):
    """unsafe helper to retrieve objects from sql
    """
    with session_scope() as session:
        return session.execute(sql_string.format(*args, **kwds))


% for model in data.schema.models:

% if model.enum_fields:
% for field in model.enum_fields:

${field.name.upper()} = Enum(
% for key, _ in data.schema.enums[field.name].items():
    ${key.quote},
% endfor
    name='${field.name}')

% endfor
% endif
% endfor

% for model in data.schema.models:


class ${model.name.classname}(Base):
    __tablename__ = '${model.name}'

    % for field in model.fields:
    ${field.definition}
    % endfor


% endfor


<%block name="model_data">
% if not data.options.models_only:

# ${data.schema.name} DATA
# ---------------------------------------------------------------

% for model in data.schema.models:
% if model.data:
${model.name.plural()} = [
% for row in model.data:
    ${model.classname}(${model.row_dict(row)}),
% endfor
]

% endif
% endfor




if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = Session()
    % for model in data.schema.models:
    % if model.data:
    session.add_all(${model.name.plural()})
    % endif
    % endfor
    session.commit()

% endif
</%block>
