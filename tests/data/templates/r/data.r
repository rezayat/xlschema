#' ${data.schema.name}

% for model in data.schema.models:
#' data.table of ${model.name}
#'
#' <description of object class>
#'
#' @format A data.table with n rows and ${len(model.fieldnames)} variables:
#' \describe{
% for field in model.number_fields:
#'   \item{${field.name}} {${field.description}}
% endfor
#' }
"${model.name}"
% endfor
