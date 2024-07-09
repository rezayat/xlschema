import os
import records

DBI_URI = os.getenv('DBI_URI', '${data.config.DB_URI}')

db = records.Database(DBI_URI)

# ${data.schema.name} SCHEMA
# ---------------------------------------------------------------

% for model in data.schema.models:

${model.name.plural()} = db.query('select * from ${model.name}')

% endfor
