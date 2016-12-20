from rancher.engine import Model
import pytest


class TestBaseModel:

    @pytest.mark.skip
    def test_init_not_populates_attributes(self):
        class Inherited(Model):
            attr1 = "None"

        inherited = Inherited(attr1="lol")

        assert inherited.attr1 == "None"

    def test_init_not_populates_not_provided_class(self):
        class MyModel2(Model):
            atr1 = "lol"

        class MyModel(Model):
            atr1 = "Nothing"
            atr2 = MyModel2

        instance = MyModel(atr1="none")

        assert not instance.atr2

    def test_init_checks_argument_for_model_class(self):
        class MyModel2(Model):
            atr = "Nothing"

        class MyModel(Model):
            atr = MyModel2
        with pytest.raises(Exception):
            instance = MyModel(atr='none')

    def test_init_populates_declared_field(self):
        class Inherited(Model):
            attr1 = ""

        inherited = Inherited(attr1="test")

        assert inherited.attr1 == "test"
