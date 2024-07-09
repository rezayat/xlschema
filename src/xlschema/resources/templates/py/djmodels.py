from datetime import datetime
from django.db import models

% for model in data.schema.models:

# ${model.name.upper()}
# ----------------------------------------------------------
% if model.enum_fields:
% for field in model.enum_fields:

${field.name.upper()} = [
    % for key, val in data.schema.enums[field._name].items():
    % if data.schema.enums[field._name].type == 'str':
    (${key.quote}, ${val.quote}),
    % else:
    (${key}, ${val.quote}),
    % endif
    % endfor
]

% endfor
% endif


class ${model.name.classname}(models.Model):
    % for field in model.fields:
    ${field.definition}
    % endfor

    class Meta:
        db_table = "${model.name}"
        verbose_name_plural = "${model.name.plural()}"

    def __str__(self):
        return "${model.classname}-{}".format(self.id)

% endfor
