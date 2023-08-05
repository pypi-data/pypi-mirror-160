from inspect import isfunction
from types import UnionType
from typing import Iterable, Callable, Any, get_origin, get_args

from .lib.utils import has_value, get_value

ValidationError = TypeError


class AbstractValidator:

    def validate(self, value, key, data):
        pass

    def __call__(self, value, key, data) -> Any:
        return self.validate(value, key, data)

    def __repr__(self):
        return f'{self.__class__.__name__}'


class BaseValidator(AbstractValidator):

    def __or__(self, other):
        return OrCombinator(self, other)

    def __and__(self, other):
        return AndCombinator(self, other)


MethodValidatorType = Callable[[Any, str | int, Any], Any]


class MethodValidator(BaseValidator):

    def __init__(self, validate: MethodValidatorType):
        self._validate = validate

    def validate(self, value, key, data):
        return self._validate(value, key, data)


class ValueValidator(BaseValidator):

    def validate(self, value, key, data):
        self.validate_value(value)

    def validate_value(self, value):
        pass


class BaseCombinator(BaseValidator):

    validators: Iterable[AbstractValidator]

    def __init__(self, *validators: AbstractValidator):
        self.validators = validators


class AndCombinator(BaseCombinator):

    def validate(self, value, key, data):
        prev = value

        for func in self.validators:
            try:
                result = func(prev, key, data)
                if result is not None:
                    prev = result
            except ValidationError as error:
                raise error

    def __repr__(self):
        return f'{super().__repr__()}[{"&".join([v.__repr__() for v in self.validators])}]'


class OrCombinator(BaseCombinator):

    def validate(self, value, key, data):
        errors = list()

        for func in self.validators:
            try:
                return func(value, key, data)
            except ValidationError as error:
                errors.append(error)

        raise errors

    def __repr__(self):
        return f'{super().__repr__()}[{"|".join([v.__repr__() for v in self.validators])}]'


class PatternValidator(BaseValidator):

    def __init__(self, *pattern, deny: bool = False):
        self.pattern = pattern
        self.deny = deny

    def validate(self, value, key, data):
        if len(self.pattern) and (value in self.pattern) == self.deny:
            raise ValidationError(f'{value} is {"deny" if self.deny else "required"} by {self.pattern}')


class IsRequired(BaseValidator):

    not_blank: bool
    blank_pattern: list = [None, '']

    def __init__(self, not_blank: bool | list = False):
        super().__init__()

        self.not_blank = not_blank
        if type(not_blank) is list:
            self.blank_pattern = not_blank

    def validate(self, value, key, data):
        if type(key) is int:
            return

        if has_value(data, key):
            if not self.not_blank or get_value(data, key) not in self.blank_pattern:
                return

        raise ValidationError(f'{key} is required')


TestType = type | Callable[[Any], bool | None]


def _create_test(origin):
    return lambda value: type(value) is origin or value is origin


class IsType(BaseValidator):

    def __init__(self, test: TestType):
        self._type_class = test

        if get_origin(test) is UnionType:
            args = get_args(test)
            self._test = lambda value: (type(value) in args or value in args)
        else:
            self._test = test if isfunction(test) else _create_test(test)

    def validate(self, value, key, data):
        if self._test(value):
            return

        raise ValidationError(f'{value} [{type(value)}] has not required type {self._type_class}')
