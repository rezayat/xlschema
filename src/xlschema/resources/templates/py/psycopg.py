from datetime import datetime
import sys
import logging as log
import psycopg2

LOG_LEVEL = log.INFO
LOG_FORMAT = '%(relativeCreated)-3d %(levelname)s: %(message)s'
log.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, stream=sys.stdout)


log.info('CONNECTING')

DBI_URI = os.getenv('DBI_URI', 'dbname=postgres user=postgres')

connection = psycopg2.connect(DBI_URI)

cursor = connection.cursor()

log.info('EXECUTING SCHEMA: ${data.schema.name}')

# ${data.schema.name} SCHEMA
# ---------------------------------------------------------------

% for model in data.schema.models:

# table ${model.name}
log.info('dropping table ${model.name}')
cursor.execute("drop table if exists ${model.name} cascade;")
log.info('creating table ${model.name}')
cursor.execute("""
    create table ${model.name}
    (
        % for definition in model.definitions:
        ${definition}
        % endfor
    );
""")

% endfor

% if not data.options.models_only:
# ${data.schema.name} DATA
# ---------------------------------------------------------------
% for model in data.schema.models:

% if model.data:
log.info('inserting data into table ${model.name}')
% for row in model.data:
cursor.execute("insert into ${model.name} values ${data.process(row)};")
% endfor
##
% endif
% endfor
% endif

# cleanup and closure
log.info('CLOSING CONNECTION')
connection.commit()
cursor.close()
connection.close()

log.info('DONE')
