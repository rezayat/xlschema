create extension if not exists pgtap;

BEGIN;
select no_plan();

-- START tests here
-- ------------------------------------

% for model in data.schema.models:
select diag('Testing ${model.name} Table');
select has_table('${model.name}');
select isnt_empty('select * from ${model.name}', 'Table ${model.name} is not empty');

% endfor



-- --------------------------------
-- END tests here

select * from finish();
ROLLBACK;
