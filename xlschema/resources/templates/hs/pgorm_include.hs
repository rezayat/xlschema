<%def name="render_model(model)">
-- ---------------------------------------------------------------
-- ${model.classname} Model
-- ---------------------------------------------------------------

data ${model.classname} = ${model.classname}
    % for field in model.fields:
    % if field.is_pk:
    { ${field.definition}
    % else:
    , ${field.definition}
    % endif
    % endfor
    } deriving (Show, Generic)

instance Model ${model.classname} where
    modelInfo = underscoreModelInfo (fromString "${model.name}")

instance FromRow ${model.classname} where
    fromRow = ${model.classname}
           <$> field
    % for i in model.mapped_fields:
           <*> field
    % endfor


instance ToRow ${model.classname} where
    toRow i = [ toField $ ${model.name.camelcase}ID i
    % for field in model.mapped_fields:
              , toField $ ${field.name} i
    % endfor
              ]

% if model.enum_fields:
% for field in model.enum_fields:

instance FromField ${field.name.classname} where
    fromField f mdata = do
        x <- fromField f mdata
        case x :: ${field.type} of
        % for key, val in data.schema.enums[field._name].items():
            % if field.type == "String":
            ${key.quote} -> return ${val.classname}
            % else:
            ${key} -> return ${val.classname}
            % endif
        % endfor
            _   -> mzero

instance ToField ${field.name.classname} where
    toField x = case x of
        % for key, val in data.schema.enums[field._name].items():
        % if field.type == "String":
        ${val.classname} -> Escape ${key.quote}
        % else:
        ${val.classname} -> Plain (intDec ${key})
        % endif
        % endfor

% endfor
% endif


-- ${model.classname} utility functions

get${model.classname}s :: IO [${model.classname}]
get${model.classname}s = do
    c <- getConnection
    findAll c :: IO [${model.classname}]
</%def>
