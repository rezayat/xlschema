"""DB to Model SchemaReader."""
import yaml

from ... import fields, models
from .. import abstract

# ----------------------------------------------------------
# YAML Conversion
# ----------------------------------------------------------


class YamlToModel(abstract.SchemaReader):
    """Parses yaml files into relational models."""

    def preprocess(self):
        """Runs before main process method for conversion.

        Place reader specific instance variable here
        """
        with open(self.uri, 'r') as stream:
            try:
                self.yaml = yaml.safe_load(stream=stream)
            except yaml.YAMLError as exc:
                self.log.error(str(exc))
                raise

    def _get_model_data(self, model):
        """Retrieves data dikt values in order of fields."""
        _data = []
        _fields = [field['name'] for field in model['fields']]
        for row in model['data']:
            entry = tuple([row[f] for f in _fields])
            self.log.debug('%s', entry)
            _data.append(entry)
        return _data

    def _get_enums(self):
        """Retrieve enums from yaml entries."""
        if 'enums' not in self.yaml:
            self.yaml['enums'] = []
        for enum in self.yaml['enums']:
            if isinstance(enum['data'][0], dict):
                rows = [(d['key'], d['value']) for d in enum['data']]
            else:
                rows = [tuple(row) for row in enum['data']]
            self.schema.enums[enum['name']] = models.Enum(name=enum['name'],
                                                          data=rows)

    def process(self):
        """Main process for conversion."""
        self.log.debug("processing %s", self.uri)

        # enums
        self._get_enums()

        # models
        model_names = []

        for model in self.yaml['models']:

            model_names.append(model['name'])

            # check for properties
            if 'properties' not in model:
                model['properties'] = {}

            # check for data
            if 'data' not in model:
                model['data'] = []

            if model['data'] and isinstance(model['data'][0], dict):
                rows = self._get_model_data(model)
            else:
                rows = [tuple(row) for row in model['data']]

            self.schema.models.append(models.Model(
                name=model['name'],
                fields=[fields.Field.from_dict(d) for d in model['fields']],
                properties=model['properties'],
                data=rows,
            ))

        self.post_process(model_names)
