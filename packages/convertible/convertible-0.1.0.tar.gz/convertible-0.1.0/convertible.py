import typing
from typing import Generic, Optional, Type, TypeVar

__all__ = ["Convertible", "From"]

T = TypeVar("T")
S = TypeVar("S")
D = TypeVar("D")

_into_reg = {}
_from_reg = {}


class Convertible:
    def __init_subclass__(cls):
        _from_reg[(cls, dict)] = default_struct_from_dict_factory(cls)
        _into_reg[(cls, dict)] = DefaultStructIntoDict

    @classmethod
    def try_from(cls: Type[T], value: S, type_: Optional[Type[S]] = None) -> T:
        converter = _from_reg[(cls, type_ or type(value))]
        return converter().try_from(value)

    def try_into(self, target: Type[T]) -> T:
        converter = _into_reg[(type(self), target)]
        return converter().try_from(self)


class From(Generic[S, D]):
    _src = None
    _dest = None

    @typing._tp_cache
    def __class_getitem__(cls, params):
        src, dest = params

        class Proxy(cls):
            _src = src
            _dest = dest

        return Proxy

    def __init_subclass__(cls):
        cls.register_converter(cls)

    @classmethod
    def try_from(cls, value):
        converter = _from_reg[(cls._dest, cls._src)]
        return converter().try_from(value)

    @classmethod
    def register_converter(cls, conv):
        src, dest = cls._src, cls._dest

        if isinstance(src, type) and issubclass(src, Convertible):
            _into_reg[(src, dest)] = conv
        # src.register_into_converter(dest, cls)

        # if isinstance(dest, type) and issubclass(dest, Convertible):
        _from_reg[(dest, src)] = conv
        # dest.register_from_converter(src, cls)


def default_struct_from_dict_factory(target):
    class DefaultStructFromDict(From):
        def try_from(self, value: dict) -> T:
            return target(**value)

    return DefaultStructFromDict


class DefaultStructIntoDict(From):
    def try_from(self, value: Convertible) -> dict:
        return value.__dict__
