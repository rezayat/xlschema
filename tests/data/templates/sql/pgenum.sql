<%inherit file="/sql/postgres.sql"/>

<%block name="schema">
% if not data.options.update_only:
% for model in data.schema.models:

% if model.enum_fields:
% for field in model.enum_fields:

drop type ${field.name} cascade;
create type ${field.name} as enum (
% for key, val in data.schema.enums[field.name].items():
    % if loop.last:
    '${key}'
    % else:
    '${key}',
    % endif
% endfor
);

% endfor
% endif

drop table if exists ${model.name} cascade;
create table ${model.name}
(
    % for definition in model.definitions:
    ${definition}
    % endfor
);

% endfor
% endif
</%block>
