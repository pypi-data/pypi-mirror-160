from inspect import ismethod, signature
from types import UnionType
from typing import Any, TypeVar, Generic

from .field import BaseField, MethodField, Undefined, ObjectField, Field, UnionField, IterableField
from .interfacies import AbstractSerializer
from .lib.utils import get_instance_members, get_value, get_annotations, inspect_annotations


def _tuple(value, custom_name):
    return value if type(value) == tuple else (value, custom_name)


def _member_factory_wrapper(member, self=None):
    return (lambda d, k: _tuple(member(self, d), None)) if self else (lambda d, k: _tuple(member(d), None))


def _is_type_support(any_type):
    return issubclass(any_type, AbstractSerializer) or issubclass(any_type, BaseField)


def _parse_annotation(annotation_data):
    if type(annotation_data) is type:
        if _is_type_support(annotation_data):
            return ObjectField(origin=annotation_data, is_required=True)
        else:
            return Field(is_type=annotation_data)
    elif isinstance(annotation_data, dict):
        origin = annotation_data['origin']
        args = annotation_data['args']

        if origin is UnionType:
            fields = [_parse_annotation(a) for a in args]
            return UnionField(*fields)
        elif origin is list:
            field_prototype = _parse_annotation(args[0])
            return IterableField(origin=field_prototype, is_required=True)

    return Field()


def _parse_annotations(annotations_data):
    return {key: _parse_annotation(field) for key, field in annotations_data.items()}


class BaseSerializer(AbstractSerializer):

    __cached_fields: dict[str, BaseField] | None = None

    @classmethod
    def __cache__(cls):
        if cls.__cached_fields:
            return cls.__cached_fields

        cached_fields = dict()

        # Annotations parser
        annotations_data = inspect_annotations(get_annotations(cls))
        annotation_fields = _parse_annotations(annotations_data)

        for key, field in annotation_fields.items():
            cached_fields[key] = field

        # Members parser
        members = get_instance_members(cls, Deserializer)

        for key, member in members:
            if isinstance(member, BaseField):
                cached_fields[key] = member
            elif ismethod(member):
                cached_fields[key] = MethodField(factory=_member_factory_wrapper(member))
            else:
                cached_fields[key] = MethodField(factory=_member_factory_wrapper(member, cls))

        cls.__cached_fields = cached_fields
        return cached_fields

    @classmethod
    def init(cls, data):
        return {}

    @classmethod
    def apply(cls, result, key, value, data):
        result[key] = value

    @classmethod
    def serialize(cls, data):
        result = cls.init(data)
        cached_fields = cls.__cache__()

        for key, field in cached_fields.items():
            value, name = field(data, key)

            if value is not Undefined:
                cls.apply(result, name or key, value, data)

        return result


class Serializer(BaseSerializer):

    def serialize(self, data):
        init_data = super(Serializer, self).serialize(data)
        return init_data


X = TypeVar('X', bound=Any)


class Deserializer(Serializer, Generic[X]):

    prototype = None

    def __init__(self, prototype=None):
        self.prototype = prototype

    def create(self, data, prototype=None) -> X:
        init_data = self.serialize(data)

        current_proto = prototype or self.prototype
        if not current_proto:
            raise TypeError('Prototype is required')

        init_args = list(signature(current_proto.__init__).parameters.keys())[1:]

        return current_proto(
            **{
                key: get_value(init_data, key)
                for key in init_args
                if key in init_data or hasattr(init_data, key)
            }
        )
