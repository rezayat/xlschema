import os
import pandas

DB_URI = os.getenv('DB_URI', '${data.config.DB_URI}')


# ${data.schema.name} SCHEMA
# ---------------------------------------------------------------

% for model in data.schema.models:

${model.name.plural()} = pandas.read_sql_table('${model.name}', DB_URI)

% endfor
