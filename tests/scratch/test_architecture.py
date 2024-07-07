from typing import Dict, List, Any


class Field:
    def __init__(self, name: str, options: dict = None) -> None:
        self.name = name
        self.options = options


class Namespace:
    def __init__(self, parent: 'Model') -> None:
        self.parent = parent


class Model:
    def __init__(self,
                 name: str,
                 fields: List[Field] = None,
                 data: List[Any] = None,
                 properties: dict = None,
                 metadata: dict = None,
                 options: dict = None,
                 nspace_class: Namespace = None) -> None:
        self.name = name
        self.fields = fields
        self.data = data
        self.properties = properties
        self.metadata = metadata
        self.options = options
        self.nspace_class = nspace_class


class Enum:
    def __init__(self, name: str, data: List[Any] = None) -> None:
        self.name = name
        self.data = data


class Schema:
    def __init__(self,
                 name: str,
                 models: List[Model] = None,
                 enums: Dict[str, Enum] = None,
                 options: dict = None) -> None:
        self.name = name
        self.models = models
        self.enums = enums
        self.options = options


def get_schema():
    model = Model(
        name='person',
        fields=[
            Field('name'),
            Field('age'),
        ],
        data=[
            ('sam', 10),
            ('jon', 14),
        ],
        properties=dict(
            app='com.acme.core.person',
            model='com.acme.core.person.models.Person'),
        metadata=dict(created='2017-11-14'),
        options=dict(),
        nspace_class=Namespace)
    enum = Enum(name='state', data=[('a', 'SUCCESS'), ('b', 'FAIL')])

    schema = Schema(
        name='myschema',
        models=[model],
        enums=dict(state=enum),
        options=dict(),
    )

    return schema


class SchemaWriter:
    model_class = None
    nspace_class = None
    field_class = None
    file_suffix = None
    method = None

    def __init__(self, schema: Schema, options: dict = None) -> None:
        self.schema = schema
        self.options = options

    def run(self) -> None:
        """Default run method."""

    def write(self, to_path: str = None) -> None:
        """Core workhorse method."""


class SchemaReader:
    def __init__(self, uri: str, options: dict = None) -> None:
        self.uri = uri
        self.options = options
        self.schema = get_schema()

    def preprocess(self) -> None:
        """Runs before main process for conversion."""

    def process(self) -> None:
        """Main process for conversion."""

    def post_process(self, model_names: List[str]) -> None:
        """Creates a set of all types used in the schema."""


class Application:
    def __init__(self, uri: str, options: dict = None) -> None:
        self.uri = uri
        self.schema = self.get_reader(uri, options).schema
        self.options = options

    def get_reader(self, uri: str, options: dict = None,
                   **kwds: dict) -> SchemaReader:
        """Returns a specialized schema reader based parsed uri."""
        return SchemaReader(uri, options)

    def get_writer(self, writer_type: str) -> SchemaWriter:
        """Get a special writer based on type."""
        return SchemaWriter(self.schema, self.options)

    def write(self, *writer_types: str, to_path: str = None) -> None:
        """Execute write operation of writer(s)."""

    def run(self, *writer_types: str):
        """Run all default operations of writer(s)."""

    def populate(self, *writer_types: str):
        """Execute populate operation of writer(s)."""


def test_architecture(mocker):
    app = Application(uri='/tmp/file.py')

    mocker.patch.object(app, 'write')
    app.write.return_value = 'HELLO WORLD'
    assert app.write() == 'HELLO WORLD'

    assert app.schema
    writer = app.get_writer(writer_type='sql/sqlite')
    assert writer.schema
