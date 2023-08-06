import enum
import typing as tp

from abc import ABCMeta, abstractmethod

from .patterns import _Singleton


class _Comparable(metaclass=ABCMeta):
    @abstractmethod
    def __lt__(self, other: tp.Any) -> bool: ...


CT = tp.TypeVar('CT', bound=_Comparable)


class Bound(enum.Enum):
    """
    Bound types.
    """
    OPEN = False
    CLOSED = True

    def bracket(self, is_left: bool = True) -> str:
        if self.value:
            return "[" if is_left else "]"

        return "(" if is_left else ")"

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class _PositiveInf(_Singleton):
    """
    Positive infinity.
    """
    def __neg__(self) -> '_NegativeInf':
        return _NegativeInf()

    def __lt__(self, other: CT) -> bool:
        return False

    def __le__(self, other: CT) -> bool:
        return isinstance(other, _PositiveInf)

    def __gt__(self, other: CT) -> bool:
        return True

    def __ge__(self, other: CT) -> bool:
        return not isinstance(other, _PositiveInf)

    def __eq__(self, other: CT) -> bool:
        return isinstance(other, _PositiveInf)

    def __repr__(self):
        return "inf"

    def __add__(self, other: CT) -> '_PositiveInf':
        if isinstance(other, _NegativeInf):
            raise ValueError("Undefined sum of positive and negative infinities")

        return self

    def __sub__(self, other: CT) -> '_PositiveInf':
        if isinstance(other, _PositiveInf):
            raise ValueError("Undefined difference of positive and negative infinities")

        return self

    def __hash__(self):
        return hash(float("inf"))


class _NegativeInf(_Singleton):
    """
    Negative infinity
    """

    def __neg__(self) -> '_PositiveInf':
        return _PositiveInf()

    def __lt__(self, other: CT) -> bool:
        return True

    def __le__(self, other: CT) -> bool:
        return not isinstance(other, _NegativeInf)

    def __gt__(self, other: CT) -> bool:
        return False

    def __ge__(self, other: CT) -> bool:
        return isinstance(other, _NegativeInf)

    def __eq__(self, other: CT) -> bool:
        return isinstance(other, _NegativeInf)

    def __repr__(self):
        return "-inf"

    def __add__(self, other: CT) -> '_NegativeInf':
        if isinstance(other, _PositiveInf):
            raise ValueError("Undefined sum of positive and negative infinities")

        return self

    def __sub__(self, other: CT) -> '_NegativeInf':
        if isinstance(other, _NegativeInf):
            raise ValueError("Undefined difference of negative and positive infinities")

        return self

    def __hash__(self):
        return hash(float("-inf"))


def convert_json_value(value: tp.Any) -> tp.Any:
    if value == "inf":
        return inf
    elif value == "-inf":
        return -inf
    else:
        return value


inf = _PositiveInf()


__all__ = ['CT', 'Bound', 'inf', 'convert_json_value']