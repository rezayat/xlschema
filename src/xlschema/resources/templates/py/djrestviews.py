from rest_framework import generics

% for model in data.schema.models:

# ${model.name.upper()}
# ----------------------------------------------------------
from ${model.properties['app']}.models import ${model.classname}
from ${model.properties['app']}.serializers import ${model.classname}Serializer

class ${model.classname}List(generics.ListCreateAPIView):
    queryset = ${model.classname}.objects.all()
    serializer_class = ${model.classname}Serializer


class ${model.classname}Detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ${model.classname}.objects.all()
    serializer_class = ${model.classname}Serializer


% endfor
