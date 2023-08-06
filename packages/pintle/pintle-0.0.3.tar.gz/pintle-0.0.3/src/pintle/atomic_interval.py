import typing as tp

import json
import warnings
import plotly.figure_factory as ff

from src.pintle.bounds import *
from src.pintle.exception import AtomicIntervalException, AtomicIntervalWarning
from src.pintle.colors.colors import generate_colors


class AtomicInterval:
    def __init__(self, *args: tp.Union[Bound, CT, None]):
        """
        Atomic interval is simple interval with 2 types of bounds. Each bound is either open or closed.
        It is worth mentioning that one point is an atomic interval
        """
        assert len(args) in [0, 1, 2, 4], \
            AtomicIntervalException(f"Wrong number of arguments. The number of arguments should be 0, 1, 2 or 4")

        if len(args) == 0:
            self._init_empty_interval()

        elif len(args) == 1:
            self._init_interval(Bound.CLOSED, args[0], args[0], Bound.CLOSED)

        elif len(args) == 2:
            if args[0] > args[1]:
                warnings.warn(
                    f"""
                    Empty interval created as the left value of the interval {args[0]} 
                    is greater than the right value {args[1]} of the interval""",
                    AtomicIntervalWarning
                )
                self._init_empty_interval()
            else:
                self._init_interval(Bound.OPEN, *args, Bound.OPEN)

        else:
            if args[1] > args[2]:
                warnings.warn(
                    f"""
                    Empty interval created as the left value of the interval {args[0]} 
                    is greater than the right value {args[1]} of the interval""",
                    AtomicIntervalWarning
                )
                self._init_empty_interval()

            else:
                self._init_interval(*args)

                if self._left_value == self.right_value and \
                   (self._left_bound == Bound.OPEN or self._right_bound == Bound.OPEN):

                    self._init_empty_interval()

    def _init_empty_interval(self) -> None:
        """
        Init params of empty interval
        """
        self._left_value, self._right_value = None, None
        self._left_bound, self._right_bound = Bound.OPEN, Bound.OPEN

    def _init_interval(self, *args) -> None:
        """
        Init params of not empty interval
        """
        self._left_bound, self._left_value, self._right_value, self._right_bound = args

    def __repr__(self) -> str:
        """
        Returns the atomic interval representation. For example [0, 1), [2, +inf) or [3]
        """
        left_bracket = self._left_bound.bracket(is_left=True)
        right_bracket = self._right_bound.bracket(is_left=False)

        if self._left_value == self._right_value:
            return f"{left_bracket}{self._left_value}{right_bracket}"

        return f"{left_bracket}{self._left_value}, {self._right_value}{right_bracket}"

    def mergeable(self, b: 'AtomicInterval') -> bool:
        """
        Check if 2 atomic intervals could be merged.
        """
        if self.empty or b.empty:
            return True

        first, second = sorted((self, b), key=lambda x: x.left_value)

        if first.right_value == second.left_value:
            return first.right_bound == Bound.CLOSED or second.left_bound == Bound.CLOSED

        return first.right_value > second.left_value

    @property
    def is_extended(self) -> bool:
        f"""
        Check if {inf} or {-inf} is inside atomic interval
        :return: True if {inf} or {-inf} is inside atomic interval, False otherwise
        """
        if self.left_bound == Bound.CLOSED and self.left_value == -inf:
            return True

        if self.right_bound == Bound.CLOSED and self.right_value == inf:
            return True

        return False

    @property
    def left_bound(self) -> Bound:
        """
        Left bound of atomic interval
        """
        return self._left_bound

    @property
    def right_bound(self) -> Bound:
        """
        Right bound of atomic interval
        """
        return self._right_bound

    @property
    def left_value(self) -> CT:
        """
        Left value of atomic interval
        """
        return self._left_value

    @property
    def right_value(self) -> CT:
        """
        Right bound of atomic interval
        """
        return self._right_value

    @property
    def empty(self) -> bool:
        """
        Check if interval is empty (doesn't contain any point)
        """
        if (self._left_value is None) or (self._right_value is None):
            return True

        return False

    @property
    def length(self) -> float:
        """
        Length of interval. If interval is [inf, inf] or [-inf, -inf], the property length would return 0
        :return:
        """
        if self.empty:
            return 0

        if hasattr(self._left_value, '__sub__') and hasattr(self._right_value, '__sub__'):
            if self._right_value == inf:
                return inf

            elif self._left_value == -inf:
                return inf

            else:
                return self._right_value - self._left_value
        else:
            raise AtomicIntervalException(
                f"Unsupported operand type(s) for -: {type(self._left_value)} and {type(self._right_value)}"
            )

    def closure(self, is_extended: tp.Optional[bool] = None) -> 'AtomicInterval':
        """
        Closure of atomic interval. For example, (0, 1) -> [0, 1]
        """
        if self.empty:
            return self.__class__()

        is_extended = self.is_extended if is_extended is None else is_extended

        if is_extended:
            left_bound, right_bound = Bound.CLOSED, Bound.CLOSED
        else:
            left_bound: Bound = Bound.CLOSED if self._left_value != -inf else self._left_bound
            right_bound: Bound = Bound.CLOSED if self._right_value != inf else self._right_bound

        return self.__class__(left_bound, self.left_value, self.right_value, right_bound)

    def boundary(self, is_extended: tp.Optional[bool] = None) -> tp.List['AtomicInterval']:
        """
        Returns boundary of atomic interval
        """
        if self.empty:
            return []

        is_extended = self.is_extended if is_extended is None else is_extended
        if is_extended:
            if self._left_value == self._right_value:
                return [self.__class__(self._left_value)]
            else:
                return [self.__class__(self._left_value), self.__class__(self._right_value)]
        else:
            boundary_intervals: tp.List['AtomicInterval'] = []

            if self._left_value != -inf:
                boundary_intervals.append(self.__class__(self._left_value))

            if self._right_value != inf and self._right_value != self.left_value:
                boundary_intervals.append(self.__class__(self._right_value))

            return boundary_intervals

    def interior(self) -> 'AtomicInterval':
        """
        Returns the interior of atomic interval.
        """
        if self._left_value == self._right_value:
            return self.__class__()

        return self.__class__(Bound.OPEN, self._left_value, self._right_value, Bound.OPEN)

    def intersected(self, other: 'AtomicInterval') -> bool:
        """
        Check if two intervals are intersecting
        """
        if self.empty or other.empty:
            return False

        first, second = sorted((self, other), key=lambda x: (x.left_value, x.right_value))

        if first.right_value == second.left_value:
            return first.right_bound == Bound.CLOSED and second.left_bound == Bound.CLOSED

        return first.right_value > second.left_value

    def adjacent(self, other: 'AtomicInterval') -> bool:
        """
        Check if two intervals are not intersected but mergeable.
        """
        if self.empty or other.empty:
            return True

        first, second = sorted((self, other), key=lambda x: (x.left_value, x.right_value))
        if first.right_value == second.left_value:
            return int(first.right_bound == Bound.CLOSED) + int(second.left_bound == Bound.CLOSED) == 1

        return False

    def apply(self,
              left_bound: tp.Callable[[Bound], Bound] = None,
              left_value: tp.Callable[[CT], CT] = None,
              right_value: tp.Callable[[CT], CT] = None,
              right_bound: tp.Callable[[Bound], Bound] = None,
              ignore_inf: bool = True,
              ) -> 'AtomicInterval':
        """
        Apply some function on right and left values of interval. Return new atomic interval
        """
        if self.empty:
            return self

        l_bound = self._left_bound if not left_bound else left_bound(self._left_bound)

        if left_value is not None:
            if ignore_inf and (self._left_value == inf or self._left_value == -inf):
                l_value = self._left_value
            else:
                l_value = left_value(self._left_value)
        else:
            l_value = self._left_value

        if right_value is not None:
            if ignore_inf and (self._right_value == inf or self._right_value == -inf):
                r_value = self._right_value
            else:
                r_value = right_value(self._right_value)
        else:
            r_value = self._right_value

        r_bound = self._right_bound if not right_bound else right_bound(self._right_bound)

        return self.__class__(l_bound, l_value, r_value, r_bound)

    def trim(self, value: CT, to_right=True) -> 'AtomicInterval':
        """
        Cut the atomic interval. For example, if interval is [0, 5], value = 3 and to_right=True,
        the result would be [3, 5].
        """
        if value in self:
            if to_right:
                return AtomicInterval(Bound.CLOSED, value, self._right_value, self._right_bound)
            else:
                return AtomicInterval(self._left_bound, self._left_value, value, Bound.CLOSED)

        if to_right:
            return AtomicInterval() if value >= self._right_value else self
        else:
            return AtomicInterval() if value <= self._left_value else self

    def to_json(self) -> tp.Mapping[str, tp.Union[str, float, int]]:
        """
        #todo: datetime
        Convert  atomic interval to json
        :return: dictionary with interval parameters
        """
        if self.empty:
            return {}
        else:
            return {
                'left_bound': self._left_bound.name,
                'left_value': self._left_value if isinstance(self._left_value, (float, int)) else str(self._left_value),
                'right_value': self._right_value if isinstance(self._right_value, (float, int)) else str(self._right_value),
                'right_bound': self._right_bound.name,
            }

    @classmethod
    def from_json(cls, json_obj: tp.Union[str, tp.Mapping[str, tp.Any]]):
        """
        Build atomic interval from json object
        :param json_obj: json object
        :return: atomic interval
        """
        if isinstance(json_obj, str):
            json_obj = json.loads(json_obj)

        if not isinstance(json_obj, dict):
            raise AtomicIntervalException("""
                Wrong format of json data. Shoud be dictionary with
                - left_bound,
                
                """)

        if not json_obj:
            return cls()
        else:
            left_bound = Bound.CLOSED if json_obj['left_bound'] == 'CLOSED' else Bound.OPEN
            left_value = convert_json_value(json_obj['left_value'])
            right_value = convert_json_value(json_obj['right_value'])
            right_bound = Bound.CLOSED if json_obj['right_bound'] == 'CLOSED' else Bound.OPEN

            return cls(left_bound, left_value, right_value, right_bound)

    def __len__(self) -> int:
        return int(self.empty)

    def __iter__(self) -> 'AtomicInterval':
        yield self

    def __and__(self, other: 'AtomicInterval') -> 'AtomicInterval':
        if not self.intersected(other):
            return AtomicInterval()

        left_value = max(self._left_value, other._left_value)
        right_value = min(self._right_value, other._right_value)

        left_bound, right_bound = Bound.CLOSED, Bound.CLOSED

        for x in [self, other]:
            if x.left_value == left_value and left_bound != Bound.OPEN:
                left_bound = x.left_bound

            if x.right_value == right_value and right_bound != Bound.OPEN:
                right_bound = x.right_bound

        return AtomicInterval(left_bound, left_value, right_value, right_bound)

    def __or__(self, other: 'AtomicInterval') -> 'AtomicInterval':
        if not self.mergeable(other):
            raise AtomicIntervalException("Two intervals can't be merged")

        if self.empty:
            return other

        if other.empty:
            return other

        left_value = min(self._left_value, other._left_value)
        right_value = max(self._right_value, other._right_value)

        left_bound, right_bound = Bound.OPEN, Bound.OPEN

        for x in [self, other]:
            if x.left_value == left_value and left_bound != Bound.CLOSED:
                left_bound = x.left_bound

            if x.right_value == right_value and right_bound != Bound.CLOSED:
                right_bound = x.right_bound

        return AtomicInterval(left_bound, left_value, right_value, right_bound)

    def __contains__(self, other: tp.Union['AtomicInterval', CT]) -> bool:
        # todo: refactor!!!!
        if self.empty:
            return False

        if not isinstance(other, self.__class__):
            other = AtomicInterval(other)

        if self._left_value > other.left_value or self._right_value < other.right_value:
            return False

        if other._left_value == self._left_value and other.left_bound.value > self.left_bound.value:
            return False

        if other._right_value == self._right_value and other.right_bound.value > self.right_bound.value:
            return False

        return True

    def __add__(self, other: 'AtomicInterval') -> 'AtomicInterval':
        return self | other

    def __sub__(self, other):
        return self & other

    def __lt__(self, other: 'AtomicInterval') -> bool:
        return self.right_value <= other.left_value and not self.intersected(other)

    def __eq__(self, other: 'AtomicInterval') -> bool:
        return (self._left_value == other.left_value) and \
            (self._right_value == other.right_value) and \
            (self._left_bound == other.left_bound) and \
            (self._right_bound == other.right_bound)

    def __hash__(self):
        return hash(
            tuple(
                [
                    self.left_bound,
                    self.left_value,
                    self.right_value,
                    self.right_bound,
                ]
            )
        )

    def visualize(self, **kwargs):
        if self.empty:
            raise AtomicIntervalException("Can't visualize empty atomic interval")

        xaxis_dict = {'tickmode': 'array'}

        if self._left_value == -inf and self._right_value == inf:
            interval = (0, 1)
            xaxis_dict.update(
                dict(
                    tickvals=interval,
                    ticktext=('-inf', 'inf'),
                )
            )
        elif self._left_value == -inf:
            interval = (self._right_value - 1, self._right_value)
            xaxis_dict.update(
                dict(
                    tickvals=interval,
                    ticktext=('-inf', self._right_value),
                )
            )
        elif self._right_value == inf:
            interval = (self._left_value, self._left_value + 1)
            xaxis_dict.update(
                dict(
                    tickvals=interval,
                    ticktext=(self._left_value, 'inf'),
                )
            )
        else:
            interval = (self._left_value, self._right_value)

        fig = ff.create_gantt(
            [dict(Task="AtomicInterval", Start=interval[0], Finish=interval[1], Interval=str(self))],
            colors={str(self): generate_colors(1)[0]},
            index_col='Interval',
            group_tasks=True,
            height=250,
            title=f'Atomic interval {str(self)}',
            showgrid_x=True,
            bar_width=0.5
        )
        # todo: xaxis type
        fig.update_layout(
            xaxis_type='linear',
            xaxis=xaxis_dict,
            yaxis_visible=False,
        )
        return fig


__all__ = ['AtomicInterval']