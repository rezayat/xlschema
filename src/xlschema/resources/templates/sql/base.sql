<%block name="schema">
-- ${data.schema.name} SCHEMA
-- ---------------------------------------------------------------

% if not data.options.update_only:
% for model in data.schema.models:


drop table if exists ${model.name} <%block name="cascade"> </%block>;
create table ${model.name}
(
    % for definition in model.definitions:
    ${definition}
    % endfor
);

% endfor
% endif
</%block>

<%block name="schema_data">
% if not data.options.models_only:
-- ${data.schema.name} DATA
-- ---------------------------------------------------------------
% for model in data.schema.models:
% if model.data:

% for row in model.data:
insert into ${model.name} values ${data.process(row)};
% endfor

% endif
% endfor

% endif
</%block>
