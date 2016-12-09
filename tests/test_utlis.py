from rancher.utils import uncamelize


class TestUncamelize:

    def test_camelized_is_uncamelized(self):
        camelized = "myId"

        assert uncamelize(camelized) == "my_id"

    def test_only_first_camel_is_translated_to_underscore(self):
        camelized = "myID"

        assert uncamelize(camelized) == "my_id"
