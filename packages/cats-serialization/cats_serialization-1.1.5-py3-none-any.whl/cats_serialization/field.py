from inspect import isclass
from typing import Callable, Any, Tuple, Mapping

from .interfacies import AbstractSerializer
from .lib.utils import get_value
from .validator import BaseValidator, IsRequired, IsType, ValidationError, TestType


class Undefined:
    pass


class NoopValidator(BaseValidator):

    def __or__(self, other):
        return other

    def __and__(self, other):
        return other


class BaseFactory:

    _validator: BaseValidator

    def __init__(self, validator: BaseValidator | None = None):
        self._validator = validator or NoopValidator()

    def __call__(self, data, key: str) -> Tuple[Any, str | None]:
        value = get_value(data, key, Undefined)
        return (self._validator(value, key, data) or value), None

    @property
    def validator(self) -> BaseValidator:
        return self._validator

    @validator.setter
    def validator(self, value):
        self._validator = value or NoopValidator()

    def __repr__(self):
        return f'{self.__class__.__name__} validator={self._validator}'


FactoryType = Callable[[Any, str], Tuple[Any, str]] | BaseFactory


class BaseField:

    default: Any
    name: str | None

    factory: FactoryType

    def __init__(self, factory: FactoryType = BaseFactory(), default=None, name=None):
        self.default = default
        self.name = name

        self.factory = factory

    def __call__(self, data, key) -> Tuple[Any, str | None]:
        field, custom_name = self.factory(data, key)

        return (self.default if field is None else field), (self.name or custom_name)

    def __or__(self, other):
        return UnionField(self, other)


class MethodField(BaseField):
    # system field
    pass


class Field(BaseField):
    # main field util

    def __init__(
        self,
        validator: BaseValidator | None = None,
        is_required: bool = False,
        factory: BaseFactory | None = None,
        is_type: TestType | None = None,
        **kwargs
    ):
        custom_factory = factory if factory else BaseFactory(validator=validator or NoopValidator())

        if validator and factory:
            # add validator if factory created by user
            custom_factory.validator &= validator

        if is_required:
            custom_factory.validator &= IsRequired()

        if is_type:
            custom_factory.validator &= IsType(is_type)

        super().__init__(factory=custom_factory, **kwargs)

    def __repr__(self):
        return f'{self.__class__.__name__} factories={self.factory}'


class UnionField(BaseField):

    _fields: list[BaseField]

    def __init__(self, *fields: BaseField, factory=None, **kwargs):
        self._fields = list(fields)

        def custom_factory(data, key):
            in_ = 0
            for field in self._fields:
                try:
                    return field(data, key)
                except ValidationError:
                    continue

            raise ValidationError(f'No field found for {key}')

        super().__init__(factory=custom_factory, **kwargs)

    def __or__(self, other):
        self._fields.append(other)
        return self


def _pick_value(func):
    def pick(*args):
        value, name = func(*args)
        return value

    return pick


def _create_origin_factory(origin) -> Callable[[Any, str | int], Any]:
    if isinstance(origin, AbstractSerializer):
        return lambda data, key: origin.serialize(get_value(data, key))
    elif isclass(origin) and issubclass(origin, AbstractSerializer):
        return lambda data, key: origin.serialize(get_value(data, key))
    elif isinstance(origin, BaseField):
        return _pick_value(origin)
    elif isclass(origin) and issubclass(origin, BaseField):
        return _pick_value(origin())
    else:
        return lambda data, key: origin(get_value(data, key))


class IterableField(Field):

    def __init__(self, origin: type | AbstractSerializer | BaseField, **kwargs):
        self._origin_factory = _create_origin_factory(origin)

        super().__init__(**kwargs)

    def __call__(self, *args):
        data_iterable, custom_name = super().__call__(*args)

        if data_iterable is Undefined or data_iterable is None:
            return data_iterable, custom_name

        if isinstance(data_iterable, set):
            data_iterable = list(data_iterable)

        if isinstance(data_iterable, Mapping):
            return {
                key: self._origin_factory(data_iterable, key)
                for key in data_iterable
            }, custom_name
        else:
            return [
                self._origin_factory(data_iterable, index)
                for index in range(len(data_iterable))
            ], custom_name


class ObjectField(Field):

    def __init__(self, origin: type | AbstractSerializer | BaseField, **kwargs):
        self._origin_factory = _create_origin_factory(origin)

        super().__init__(**kwargs)

    def __call__(self, *args):
        data_iterable, custom_name = super().__call__(*args)

        return self._origin_factory(*args), custom_name
