from rancher.api import Model, Field

class TestBaseField:

    def test_default_value(self):
        class MyModel(Model):
            myattr = Field(default="lol")

        model_instance = MyModel()

        assert model_instance.myattr == "lol"
