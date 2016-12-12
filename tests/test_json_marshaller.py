from rancher.engine import JsonMarshable, Model


class Drawing(Model, JsonMarshable):
    drawing_name = str


class Artist(Model, JsonMarshable):
    id = None
    name = None
    drawing = Drawing


class TestJsonIsMarshalledTest:

    def test_fields_are_marshalled_to_dict(self):
        model = Artist(id="123as", name="Test model")
        marshalled = model.to_dict()

        assert marshalled['id'] == "123as"
        assert marshalled['name'] == "Test model"


    def test_nested_fields_are_marshalled_to_dict(self):
        model = Artist(
            id="123",
            name="Test model",
            drawing=Drawing(
                drawing_name="cool drawing"
            )
        )

        marshalled = model.to_dict()

        assert marshalled['drawing']['drawing_name'] == "cool drawing"

class TestJsonIsUnMarshalled:

    def test_from_dict(self):
        dict_repr = {
            'id': 'id1',
            'name': 'Picasso'
        }
        instance = Artist.from_dict(dict_repr)

        assert instance.id == "id1"
        assert instance.name == "Picasso"

    def test_nested_dicts(self):
        dict_repr = {
            'id': 'id1',
            'name': 'Picasso',
            'drawing': {'drawing_name': 'Que te pasas tete'},
        }
        instance = Artist.from_dict(dict_repr)

        assert isinstance(instance.drawing, Drawing)
        assert instance.drawing.drawing_name == 'Que te pasas tete'
