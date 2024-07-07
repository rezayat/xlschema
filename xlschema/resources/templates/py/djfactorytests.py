from django.test import TestCase

# Create your tests here.

% for model in data.schema.models:

# ${model.name.upper()}
# ----------------------------------------------------------
from ${model.properties['app']}.factories import ${model.classname}Factory

class ${model.classname}ModelTest(TestCase):

    def test_created(self):
        """objects are properly created
        """
        % if model.is_hierarchical:
        obj = ${model.classname}Factory.build(parent__parent__parent=None)
        % else:
        obj = ${model.classname}Factory.build()
        % endif

        % for name in model.fieldnames_stripped:
        self.assertIsNotNone(obj.${name})
        % endfor


% endfor
