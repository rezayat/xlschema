<%namespace name="orm" file="/hs/pgorm_include.hs"/>
{-# LANGUAGE FlexibleContexts  #-}
{-# LANGUAGE OverloadedStrings #-}
{-# LANGUAGE DeriveGeneric #-}

% if is_model_template:
module App.DataModel.${model.name.classname} where
% else:
module App.Schema where
% endif

import Control.Monad (mzero)
import Database.PostgreSQL.ORM.Model
    ( Model(..)
    , DBKey(..)
    , underscoreModelInfo
    , findAll
    --, save
    )
import GHC.Generics (Generic(..))

% if 'date' in data.schema.types:
import Database.PostgreSQL.Simple.Time      (Date)
% endif
import Database.PostgreSQL.Simple.FromRow   (FromRow(..), fromRow, field)
import Database.PostgreSQL.Simple.ToRow     (ToRow(..), toRow)
import Database.PostgreSQL.Simple.ToField   (ToField(..), Action(..), toField)
import Database.PostgreSQL.Simple.FromField (FromField(..), fromField)
import Data.ByteString.UTF8 (fromString)
import Data.ByteString.Builder (intDec)

import App.Core.DB (getConnection)

% if is_model_template:

-- ${model.classname} Types & Enumerations
-- ---------------------------------------------------------------

% for field in model.enum_fields:
data ${field.name.classname} =
% for (key, val) in data.schema.enums[field._name].items():
% if loop.index == 0:
      ${val.classname}
% else:
    | ${val.classname}
% endif
% endfor
      deriving (Eq, Show)

% endfor

% else:
-- Schema Types & Enumerations
-- ---------------------------------------------------------------

% for name in data.schema.enums:
data ${data.schema.enums[name].name.classname} =
% for (key, val) in data.schema.enums[name].items():
% if loop.index == 0:
      ${val.classname}
% else:
    | ${val.classname}
% endif
% endfor
      deriving (Eq, Show)

% endfor

% endif


% if is_model_template:
${orm.render_model(model)}
% else:
% for each_model in data.schema.models:
${orm.render_model(each_model)}

% endfor
% endif
