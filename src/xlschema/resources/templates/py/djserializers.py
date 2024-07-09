from rest_framework import serializers

from . import models

% for model in data.schema.models:

# ${model.name.upper()}
# ----------------------------------------------------------
class ${model.classname}Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.${model.classname}
        fields = ${model.fieldnames_stripped}

% endfor
