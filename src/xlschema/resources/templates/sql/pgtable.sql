% for dependency in model.dependencies:
${dependency}
% endfor

drop table if exists ${model.name} cascade;
create table ${model.name}
(
    % for definition in model.definitions:
    ${definition}
    % endfor
);
