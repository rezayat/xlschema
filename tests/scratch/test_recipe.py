import glob
from pprint import pprint
import yaml

from xlschema.common.templating import Template

yml = '''
env:
  ROOT: tests/data
  SOURCE: ${ROOT}/templates
  OUTPUT: ${ROOT}/output

recipes:
  - templates: ${SOURCE}/**/*.py
    writer: py/djmodels
'''

def get_recipe_from_string(content):
    dict_1 = yaml.load(content, Loader=yaml.SafeLoader)
    content_1 = Template(content).render(**dict_1['env'])
    dict_2 = yaml.load(content_1, Loader=yaml.SafeLoader)
    content_2 = Template(content).render(**dict_2['env'])
    return yaml.load(content_2, Loader=yaml.SafeLoader)

def get_recipe_from_path(path):
    with open(path) as f:
        content = f.read()
    return get_recipe_from_string(content)

def test_recipe_format():
    d1 = get_recipe_from_string(yml)
    d2 = get_recipe_from_path('tests/data/recipes/recipe.yml')
    # pprint(d1)
    # pprint(d2)
    assert d1 == d2

def test_process_glob():
    recipe = get_recipe_from_string(yml)
    for target in recipe['recipes']:
        files = glob.glob(target['templates'])
        print('files:', files)
        assert files
