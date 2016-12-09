from rancher.engine import JsonMarshable, Model


class MyModel(Model, JsonMarshable):
    id = None
    name = None


class TestJsonIsMarshalledTest:

    def test_fields_are_marshalled_to_dict(self):
        model = MyModel(id="123as", name="Test model")
        marshalled = model.to_dict()

        assert marshalled['id'] == "123as"
        assert marshalled['name'] == "Test model"


class TestJsonIsUnMarshalled:

    def test_from_dict(self):
        dict_repr = {
            'id': 'id1',
            'name': 'Picasso'
        }
        instance = MyModel.from_dict(dict_repr)

        assert instance.id == "id1"
        assert instance.name == "Picasso"
