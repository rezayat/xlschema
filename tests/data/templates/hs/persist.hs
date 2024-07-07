{-# LANGUAGE EmptyDataDecls             #-}
{-# LANGUAGE FlexibleContexts           #-}
{-# LANGUAGE GADTs                      #-}
{-# LANGUAGE GeneralizedNewtypeDeriving #-}
{-# LANGUAGE MultiParamTypeClasses      #-}
{-# LANGUAGE OverloadedStrings          #-}
{-# LANGUAGE QuasiQuotes                #-}
{-# LANGUAGE TemplateHaskell            #-}
{-# LANGUAGE TypeFamilies               #-}
import           Control.Monad.IO.Class  (liftIO)
import           Database.Persist
import           Database.Persist.Sqlite
import           Database.Persist.TH

share [mkPersist sqlSettings, mkMigrate "migrateAll"] [persistLowerCase|
% for model in data.schema.models:
${model.classname}
    % for field in model.fields:
    % if field.is_pk:
        <% continue %>
    % elif field.is_fk:
    ${field._name.camelcase} ${field._name.classname}
    % else:
    ${field._name.camelcase} ${field.type}
    % endif
    % endfor
    deriving Show

% endfor
|]

main :: IO ()
main = runSqlite ":memory:" $ do
    runMigration migrateAll
