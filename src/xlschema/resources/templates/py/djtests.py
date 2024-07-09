from django.test import TestCase

from .models import ${data.imports}

# Create your tests here.

% for model in data.schema.models:

# ${model.name.upper()}
# ----------------------------------------------------------
class ${model.classname}ModelTest(TestCase):
    ${model.name} = ${model.classname}(${model.fake_instance(data.schema.enums)})

% endfor
