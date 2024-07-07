import datetime

import factory

from . import models

% for model in data.schema.models:


# ${model.name.upper()} Factory
# ----------------------------------------------------------


class ${model.classname}Factory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.${model.classname}

    % for field in model.fields:
    ${field.definition}
    % endfor

% endfor
