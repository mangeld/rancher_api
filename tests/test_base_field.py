from rancher.api import Model, Field

class TestBaseField:

    def test_default_value(self):
        class MyModel(Model):
            myattr = Field(default="lol")

        model_instance = MyModel()

        assert model_instance.myattr == "lol"

    def test_same_field_multple_times_doesnt_collide(self):
        class MyModel(Model):
            myattr = Field()
            myattr2 = Field()

        instance = MyModel()
        instance.myattr = "lol"
        instance.myattr2 = "lel"

        assert instance.myattr != instance.myattr2
