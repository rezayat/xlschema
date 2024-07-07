<%inherit file="/sql/base.sql"/>

<%block name="cascade">cascade</%block>

<%block name="schema_data">
% if not data.options.models_only:
-- ${data.schema.name} DATA
-- ---------------------------------------------------------------
% for model in data.schema.models:
% if model.data:

COPY ${model.name} (${', '.join(model.fieldnames)}) FROM stdin;
% for row in model.data:
${data.process(row)}
% endfor
\.

% endif
% endfor

% endif
</%block>
