* -------------------------------------------------------
*
*
*
* -------------------------------------------------------


PROGRAM ${data.schema.name}.
* -------------------------------------------------------

% for model in data.schema.models:

CLASS zcl_${model.name} DEFINITION [class_options].
    PUBLIC SECTION.
        "[components]
    PROTECTED SECTION.
        "[components]
    PRIVATE SECTION.
        % for field in model.fields:
        % if loop.first:
        DATA: ${field.definition}
        % else:
              ${field.definition}
        % endif
        % endfor

ENDCLASS.

% endfor
