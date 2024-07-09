Master Data Sections
====================


% for model in data.schema.models:

${model.name.classname}
${model.line()}

${model.name.classname} Table Definition
${model.line('^', 'Table Definition')}

.. code-block:: sql

    drop table if exists ${model.name} cascade;
    create table ${model.name}
    (
        % for definition in model.definitions:
        ${definition}
        % endfor
    );


${model.name.classname} Sample Data
${model.line('^', 'Sample Data')}

.. htsql:: /${model.name}.limit(5)


% endfor
