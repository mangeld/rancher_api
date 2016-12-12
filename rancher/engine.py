import inspect

from rancher.utils import uncamelize

import requests


class Field:

    def __init__(self, default="", cast=str):
        self.values = dict()
        self.default = default
        self.cast = cast

    def __get__(self, instance, owner):
        return self.values.get(instance, self.default)

    def __set__(self, instance, value):
        self.values[instance] = value

    def __delete__(self, instance):
        del self.values[instance]


class JsonMarshable:

    uncamelize = True

    @classmethod
    def get_members(cls):
        members = inspect.getmembers(cls)
        members = filter(lambda e: not e[0].startswith("__"), members)
        members = filter(lambda e: not callable(e[1]), members)
        return {name: value for name, value in members}

    @classmethod
    def from_dict(cls, dict_repr):
        members = cls.get_members()
        instance = cls()
        for key, value in instance.repr_items(dict_repr):
            if key in members.keys():
                setattr(instance, key, value)
        return instance

    def repr_items(self, representation):
        if self.uncamelize:
            for key, value in representation.items():
                if isinstance(value, dict):
                    value = self.repr_items(value)
                yield uncamelize(key), value
        else:
            yield from representation.items()

    def to_dict(self):
        return {
            field: getattr(self, field)
            for field in self.get_members().keys()
        }


class Model:

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)


class RequestAdapter:

    def __init__(self):
        self.session = requests.Session()

    def get(self, url):
        return requests.get(url).json()

    def post(self, url):
        pass

    def delete(self, url):
        pass

    def put(self, url):
        pass
