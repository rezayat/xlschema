--REQ tables/${model.name}
% for dependency in model.dependencies:
${dependency}
% endfor


COPY ${model.name} (${', '.join(model.fieldnames)}) FROM stdin;
% for row in model.data:
${data.process(row)}
% endfor
\.
