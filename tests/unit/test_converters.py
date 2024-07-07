from xlschema.readers.abstract import SchemaReader


def test_identify_mtm_tables():
    model_names = ['person', 'vehicle', 'person_vehicle']
    mtm_tables = SchemaReader.identify_mtm_tables(model_names)
    assert mtm_tables == ['person_vehicle']
