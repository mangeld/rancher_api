from rancher.engine import Model, Field
import pytest


class TestBaseModel:

    @pytest.mark.skip
    def test_init_not_populates_attributes(self):
        class Inherited(Model):
            attr1 = "None"

        inherited = Inherited(attr1="lol")

        assert inherited.attr1 == "None"

    def test_init_populates_declared_field(self):
        class Inherited(Model):
            attr1 = Field()

        inherited = Inherited(attr1="test")

        assert inherited.attr1 == "test"
