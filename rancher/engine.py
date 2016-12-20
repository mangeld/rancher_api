import inspect
import types
from abc import ABCMeta, abstractmethod

from rancher.utils import uncamelize

import requests


class JsonMarshable:

    uncamelize = True

    @classmethod
    def get_members(cls):
        members = inspect.getmembers(cls)
        members = filter(lambda e: not e[0].startswith("__"), members)
        members = filter(lambda e: not isinstance(e[1], types.MethodType), members)
        members = filter(lambda e: not (callable(e[1]) and not inspect.isclass(e[1])), members)
        return {name: value for name, value in members}

    @classmethod
    def from_dict(cls, dict_repr):
        members = cls.get_members()
        instance = cls()
        dict_repr = instance.uncamelize_keys(dict_repr) if cls.uncamelize else dict_repr
        for key, value in dict_repr.items():
            if key in members.keys():
                if members[key] and issubclass(members[key], Model):
                    setattr(instance, key, getattr(cls, key).from_dict(value))
                    continue
                setattr(instance, key, value)
        instance._rawdata = dict_repr
        return instance

    def uncamelize_keys(self, representation):
        result = dict()
        if not representation:
            return dict()
        for key, value in representation.items():
            if isinstance(value, dict):
                value = self.uncamelize_keys(value)
            result.update({uncamelize(key): value})
        return result

    def to_dict(self):
        obj = dict()
        for field, value in self.get_members().items():
            if field in JsonMarshable.get_members():
                continue
            value_instance = getattr(self, field)

            if value_instance and inspect.isclass(value) and issubclass(value, Model):
                obj[field] = value_instance.to_dict()
            else:
                obj[field] = value_instance

        return obj


class Model:

    def __init__(self, **kwargs):
        class_members = inspect.getmembers(self.__class__)
        class_members = dict(filter(lambda e: not e[0].startswith("__"), class_members))
        is_model_class = lambda e: inspect.isclass(e) and issubclass(e, Model)
        for name, value in kwargs.items():
            # If the atribute is defined in the model as a nested model then check
            # if the object given is an instance of that class.
            if is_model_class(class_members[name]) and not isinstance(value, Model):
                raise ValueError(
                    "Attribute '{}' is defined as {} type in {}. '{}' instance was given instead."
                    .format(
                        name,
                        class_members[name].__name__,
                        self.__class__.__name__,
                        value.__class__.__name__)
                )
            setattr(self, name, value)
        # Search for nested uninitialized models and set them to None.
        for name, member in inspect.getmembers(self):
            if is_model_class(member) and not name.startswith("__"):
                setattr(self, name, None)
        #TODO: USE DEPENDENCY INJECTION FOR THE MOTHER OF GOD
        setattr(self, '_http', RequestAdapter())

    def __repr__(self):
        if hasattr(self, 'name'):
            return "<{} {}>".format(
                self.__class__.__name__,
                getattr(self, 'name')
            )
        else:
            return super().__repr__()


class HttpInterface():
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, url):
        pass

    @abstractmethod
    def post(self, url, *extra, **kwargs):
        pass

    @abstractmethod
    def delete(self, url):
        pass

    @abstractmethod
    def put(self, url):
        pass


class RequestAdapter(HttpInterface):

    def __init__(self):
        self.session = requests.Session()

    def get(self, url):
        return requests.get(url)

    def post(self, url, *extra, **kwargs):
        return requests.post(url, **kwargs)

    def delete(self, url):
        pass

    def put(self, url):
        pass
