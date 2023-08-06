import numpy as np
import typing as tp
import plotly.figure_factory as ff
import heapq

from src.pintle.atomic_interval import *
from src.pintle.bounds import inf, Bound, CT
from src.pintle.exception import IntervalsException
from src.pintle.colors.colors import generate_colors
from src.pintle.algorithms.binary_search_interval import binary_search_interval


class Intervals:
    """
    """
    def __init__(self, *intervals):
        self._intervals: tp.List[AtomicInterval] = []

    @classmethod
    def from_atomic(cls, *args: tp.Union[Bound, CT]) -> 'Intervals':
        instance = cls()
        atomic_interval = AtomicInterval(*args)

        if atomic_interval.empty:
            return instance

        instance._intervals = [atomic_interval]
        return instance

    @classmethod
    def from_atomics(cls, intervals: tp.List[AtomicInterval]) -> 'Intervals':
        instance = cls()

        intervals = [interval for interval in intervals if not interval.empty]
        intervals = sorted(intervals, key=lambda x: x.left_value)
        cur_interval = AtomicInterval()

        for interval in intervals:
            if interval.empty:
                continue

            if cur_interval.empty:
                cur_interval = interval

            elif cur_interval.mergeable(interval):
                cur_interval = cur_interval | interval

            else:
                instance._intervals.append(cur_interval)
                cur_interval = interval

        if cur_interval.empty:
            return instance

        instance._intervals.append(cur_interval)
        return instance

    @classmethod
    def open(cls, left_value: CT, right_value: CT) -> 'Intervals':
        """
        Creates atomic interval: (left_value, right_value)
        """
        return cls().from_atomic(Bound.OPEN, left_value, right_value, Bound.OPEN)

    @classmethod
    def open_closed(cls, left_value: CT, right_value: CT) -> 'Intervals':
        """
        Creates atomic interval: (left_value, right_value]
        """
        return cls().from_atomic(Bound.OPEN, left_value, right_value, Bound.CLOSED)

    @classmethod
    def closed_open(cls, left_value: CT, right_value: CT) -> 'Intervals':
        """
        Creates atomic interval: [left_value, right_value)
        """
        return cls().from_atomic(Bound.CLOSED, left_value, right_value, Bound.OPEN)

    @classmethod
    def closed(cls, left_value: CT, right_value: CT) -> 'Intervals':
        """
        Creates atomic interval: [left_value, right_value]
        """
        return cls().from_atomic(Bound.CLOSED, left_value, right_value, Bound.CLOSED)

    @classmethod
    def point(cls, value: CT) -> 'Intervals':
        """
        Creates one point interval: [value, value]
        """
        return cls().from_atomic(value)

    @classmethod
    def empty_interval(cls):
        """
        Creates empty interval
        """
        return cls().from_atomic()

    @classmethod
    def from_json(cls, json_obj: tp.Any) -> 'Intervals':
        """
        Create intervals from json
        :param json_obj: json object
        :return: intervals
        """
        if isinstance(json_obj, dict):
            return cls.from_atomics(
                [AtomicInterval.from_json(json_obj)]
            )
        elif isinstance(json_obj, list):
            return cls.from_atomics([AtomicInterval.from_json(x) for x in json_obj])
        else:
            raise  IntervalsException("Wrong value type, json_obj must be list or dict")


    @property
    def is_extended(self) -> bool:
        f"""
        Check if {inf} or {-inf} is inside intervals.
        :return: True if {inf} or {-inf} is inside atomic interval, False otherwise.
        """
        if self.empty:
            return False

        return self._intervals[0].is_extended or self._intervals[-1].is_extended

    @property
    def empty(self) -> bool:
        return len(self._intervals) == 0 or all([interval.empty for interval in self._intervals])

    @property
    def atomic(self) -> bool:
        return len(self._intervals) <= 1

    @property
    def length(self) -> float:
        return sum(interval.length for interval in self._intervals)

    @property
    def atomic_intervals(self) -> tp.List[AtomicInterval]:
        return self._intervals

    @property
    def max_bound(self) -> tp.Optional[CT]:
        if self.empty:
            return None

        return self._intervals[-1].right_value

    @property
    def min_bound(self) -> tp.Optional[CT]:
        if self.empty:
            return None

        return self._intervals[0].left_value

    def closure(self, is_extended: tp.Optional[bool] = None) -> 'Intervals':
        f"""
        The closure of a subset is the smallest closed subset. 
        Return closure of {self}.
        :param is_extended: If {None}, set this value to {self.is_extended};
                            If True, finds closure in the extended space [-inf, inf]; 
                            If False, finds closure in the space (-inf, inf).
        :return: closure of given intervals.
        """
        if self.empty:
            return self.__class__.from_atomics([])

        is_extended = self.is_extended if is_extended is None else is_extended

        closure_intervals: tp.List[AtomicInterval] = []

        iterator: tp.Iterator[AtomicInterval] = iter(self)
        cur_interval: AtomicInterval = next(iterator).closure(is_extended)

        for interval in self._intervals:
            if interval.adjacent(cur_interval):
                cur_interval = (cur_interval + interval).closure(is_extended)
            else:
                closure_intervals.append(cur_interval)
                cur_interval = interval.closure(is_extended)

        closure_intervals.append(cur_interval)
        return self.__class__.from_atomics(closure_intervals)

    def interior(self) -> 'Intervlas':
        f"""
        The interior of intervals is equal to the maximum open set in {self}.
        :return: interior of {self}
        """
        return self.__class__.from_atomics(
            [interval.interior() for interval in self]
        )

    def boundary(self, is_extended: tp.Optional[bool]) -> 'Intervals':
        """
        The boundary of intervals is equal to the boundary of intervals complement.
        :param is_extended: If {None}, set this value to {self.is_extended};
                            If True, finds closure in the extended space [-inf, inf];
                            If False, finds closure in the space (-inf, inf).
        :return: intervals boundary
        """
        if self.empty:
            return self.__class__.from_atomics([])

        boundary_intervals: tp.List[AtomicInterval] = []
        is_extended = self.is_extended if is_extended is None else is_extended
        iterator: tp.Iterator[AtomicInterval] = iter(self)

        for interval in iterator:
            b_intervals = interval.boundary(is_extended)
            if not boundary_intervals:
                boundary_intervals = b_intervals
            else:
                for b_interval in b_intervals:
                    if boundary_intervals[-1] != b_interval:
                        boundary_intervals.append(b_interval)

        return self.__class__.from_atomics(boundary_intervals)

    def trim(self, value: CT, to_right: bool = True):
        """
        Return trimmed intervals.
        :param value: trimmed boarder.
        :param to_right: the direction of trimming.
        :return: trimmed interval.
        """
        if value <= self._intervals[0].right_value:
            index = 0
        elif value >= self._intervals[-1].right_value:
            index = len(self._intervals) - 1
        else:
            l_pointer, r_pointer = 0, len(self._intervals) - 1

            while r_pointer - l_pointer > 0:
                m_pointer = (r_pointer + l_pointer) // 2
                if self._intervals[m_pointer].right_value >= value:
                    r_pointer = m_pointer
                else:
                    l_pointer = m_pointer + 1

            index = r_pointer

        if to_right:
            intervals = [self._intervals[index].trim(value, to_right)] + self._intervals[index + 1:]
        else:
            intervals = self._intervals[:index] + [self._intervals[index].trim(value, to_right)]

        return self.__class__.from_atomics(intervals)

    def apply(self,
              left_bound: tp.Callable[[Bound], Bound] = None,
              left_value: tp.Callable[[CT], CT] = None,
              right_value: tp.Callable[[CT], CT] = None,
              right_bound: tp.Callable[[Bound], Bound] = None,
              ignore_inf: bool = True, ) -> 'Intervals':
        f"""
        Apply any function to all intervals values. 
        """
        return Intervals.from_atomics(
            [
                interval.apply(
                    left_bound=left_bound,
                    left_value=left_value,
                    right_value=right_value,
                    right_bound=right_bound,
                    ignore_inf=ignore_inf) for interval in self._intervals
            ]
        )

    def to_json(self) -> tp.List[tp.Mapping[str, tp.Union[str, CT]]]:
        """
        Convert intervals to json array
        """
        return [interval.to_json() for interval in self._intervals]

    def adjacent(self, other: 'Intervals') -> bool:
        """
        2 intervals are adjacent if they aren't intersected and their union is atomic interval.
        For example [0,1), [2,3) and [1, 2) are adjacent intervals.
        :param other: other interval.
        :return: True if intervals are adjacent, False otherwise.
        """
        if not isinstance(other, Intervals):
            raise IntervalsException(f"Unsupported type {type(other)} for {other}!")

        if self.empty or other.empty:
            return other.atomic if self.empty else self.atomic

        if self.intersected(other):
            return False

        iterators: tp.List[tp.Iterator[AtomicInterval]] = [iter(self), iter(other)]

        cur_interval = AtomicInterval()
        heap: tp.List[tp.Tuple[float, AtomicInterval, int]] = Intervals._init_heap(*iterators)

        while len(heap) > 0:
            try:
                _, interval, index = heapq.heappop(heap)

                if cur_interval.empty:
                    cur_interval = interval

                elif cur_interval.adjacent(interval):
                    cur_interval = cur_interval | interval
                else:
                    return False

                next_interval = next(iterators[index])
                heapq.heappush(heap, (next_interval.left_value, next_interval, index))
            except StopIteration:
                pass

        return True

    def intersected(self, other: 'Intervals') -> bool:
        """
        Check if 2 intervals are intersected.
        :param other: other interval
        :return: True if intervals are intersected, False otherwise
        """
        if not isinstance(other, Intervals):
            raise IntervalsException(f"Unsupported type {type(other)} for {other}!")

        if self.empty or other.empty:
            return False

        iterators: tp.List[tp.Iterator[AtomicInterval]] = [iter(self), iter(other)]

        cur_interval = AtomicInterval()
        heap: tp.List[tp.Tuple[float, AtomicInterval, int]] = Intervals._init_heap(*iterators)

        while len(heap) > 0:
            try:
                _, interval, index = heapq.heappop(heap)

                if cur_interval.intersected(interval):
                    return True

                if interval not in cur_interval:
                    cur_interval = interval

                next_interval = next(iterators[index])
                heapq.heappush(heap, (next_interval.left_value, next_interval, index))
            except StopIteration:
                pass

        return False

    def complement(self, other: tp.Optional['Intervals'] = None) -> 'Intervals':
        f"""
        Construct complement to {other} interval. 
        If {other} interval is None, the complement to full set would be constructed. 
        :param other: other interval
        :return: complement to other interval
        """
        if other is None:
            other = self.__class__.open(-inf, inf)

        if not isinstance(other, Intervals):
            raise IntervalsException(f"Unsupported type {type(other)} for {other}!")

        if self.empty:
            return other

        if self._intervals[0].left_value == -inf:
            self._intervals[0].apply(left_bound=lambda _: Bound.OPEN)

        if self._intervals[-1].right_value == inf:
            self._intervals[-1].apply(right_bound=lambda _: Bound.OPEN)

        if self not in other:
            raise IntervalsException(f"""
                It is impossible to construct the complement because the interval {self} is not in {other}
            """)

        result = []
        self_iterator, other_iterator = iter(self), iter(other)
        other_atomic = next(other_iterator)

        for self_atomic in self_iterator:
            while self_atomic not in other_atomic:
                result.append(other_atomic)
                other_atomic = next(other_iterator)

            result.append(
                AtomicInterval(
                    other_atomic.left_bound,
                    other_atomic.left_value,
                    self_atomic.left_value,
                    Bound.OPEN if self_atomic.left_bound == Bound.CLOSED else Bound.CLOSED,
                )
            )

            other_atomic = AtomicInterval(
                Bound.OPEN if self_atomic.right_bound == Bound.CLOSED else Bound.CLOSED,
                self_atomic.right_value,
                other_atomic.right_value,
                other_atomic.right_bound,
            )

        result.append(other_atomic)
        for other_atomic in other_iterator:
            result.append(other_atomic)

        return self.__class__.from_atomics(result)

    def difference(self, other: 'Intervals') -> 'Intervals':
        # todo: faster?
        f"""
        Construct the difference between {self} interval and {other} interval.  
        :param other: other interval
        :return: Difference intervals 
        """
        if not isinstance(other, Intervals):
            raise IntervalsException(f"Unsupported type {type(other)} for {other}!")

        return (self & other).complement(self)

    def _contains_atomic(self, other: AtomicInterval) -> bool:
        f"""
        Test if atomic {other} interval is inside intervals {self._intervals}. 
        :param other:
        :return:
        """
        return binary_search_interval(self._intervals, other)

    @staticmethod
    def _init_heap(*iterators: tp.Iterator[AtomicInterval]) -> tp.List[tp.Tuple[float, AtomicInterval, int]]:
        """
        Heap initialization via adding the first elements of each iterator
        """
        heap: tp.List[tp.Tuple[float, AtomicInterval, int]] = []

        for i, iterator in enumerate(iterators):
            atomic_interval = next(iterator)
            heapq.heappush(heap, (atomic_interval.left_value, atomic_interval, i))

        return heap

    def __iter__(self):
        yield from self._intervals

    def __contains__(self, other: tp.Union['Intervals', CT]) -> bool:
        if not isinstance(other, Intervals):
            try:
                other = Intervals.from_atomic(other)
            except:
                raise IntervalsException(f"Unsupported type {type(other)} for {other}!")

        iterator: tp.Iterator[AtomicInterval] = iter(self)
        cur_interval: AtomicInterval = next(iterator)

        for search_interval in other.atomic_intervals:
            try:
                if search_interval in cur_interval:
                    continue

                if cur_interval > search_interval:
                    return False
                cur_interval = next(iterator)
            except StopIteration:
                return False

        return True

    def __len__(self) -> int:
        return len(self._intervals)

    def __eq__(self, other: 'Intervals') -> bool:
        return self._intervals == other._intervals

    def __repr__(self) -> str:
        return ",".join([repr(interval) for interval in self._intervals])

    def __and__(self, other: 'Intervals') -> 'Intervals':
        if self.empty or other.empty:
            return Intervals.from_atomic()

        result_interval = Intervals.from_atomic()

        iterators: tp.List[tp.Iterator[AtomicInterval]] = [iter(self), iter(other)]

        cur_interval = AtomicInterval()
        heap: tp.List[tp.Tuple[float, AtomicInterval, int]] = Intervals._init_heap(*iterators)

        while len(heap) > 0:
            try:
                _, interval, index = heapq.heappop(heap)

                if cur_interval.intersected(interval):
                    result_interval._intervals.append(cur_interval & interval)

                if interval not in cur_interval:
                    cur_interval = interval

                next_interval = next(iterators[index])
                heapq.heappush(heap, (next_interval.left_value, next_interval, index))
            except StopIteration:
                pass

        return result_interval

    def __or__(self, other: 'Intervals') -> 'Intervals':
        if self.empty:
            return other

        if other.empty:
            return self

        result_interval = Intervals.from_atomic()
        iterators: tp.List[tp.Iterator[AtomicInterval]] = [iter(self), iter(other)]

        cur_interval = AtomicInterval()
        heap: tp.List[tp.Tuple[float, AtomicInterval, int]] = Intervals._init_heap(*iterators)

        while len(heap) > 0:
            try:
                _, interval, index = heapq.heappop(heap)

                if cur_interval.empty:
                    cur_interval = interval

                elif cur_interval.mergeable(interval):
                    cur_interval = cur_interval | interval

                else:
                    result_interval._intervals.append(cur_interval)
                    cur_interval = interval

                next_interval = next(iterators[index])
                heapq.heappush(heap, (next_interval.left_value, next_interval, index))
            except StopIteration:
                pass

        if not cur_interval.empty:
            result_interval._intervals.append(cur_interval)
        return result_interval

    def __add__(self, other: 'Intervals') -> 'Intervals':
        return self | other

    def __sub__(self, other: 'Intervals') -> 'Intervals':
        return self & other

    def visualize(self, **kwargs):
        # todo: for different types of data - different visualization
        if self.empty:
            raise IntervalsException("Can't visualize empty intervals")

        left_value, right_value = 0, 0
        right_text, left_text = left_value, right_value
        data: tp.List[tp.Mapping[str, tp.Any]] = []

        for i, interval in enumerate(self._intervals):
            if interval.left_value == -inf and interval.right_value == inf:
                data.append(
                    dict(
                        Task="Interval",
                        Start=0,
                        Finish=1,
                        Interval=str(interval)
                    )
                )
                left_value, right_value = 0, 1
                right_text, left_text = '-inf', 'inf'

            elif interval.left_value == -inf:
                data.append(
                    dict(
                        Task="Interval",
                        Start=interval.right_value,
                        Finish=interval.right_value - 1,
                        Interval=str(interval)
                    )
                )
                left_value, left_text = interval.right_value - 1, '-inf'

            elif interval.right_value == inf:
                data.append(
                    dict(
                        Task="Interval",
                        Start=interval.left_value,
                        Finish=interval.left_value + 1,
                        Interval=str(interval)
                    )
                )
                right_value, right_text = interval.left_value + 1, 'inf'

            else:
                data.append(
                    dict(
                        Task="Interval",
                        Start=interval.left_value,
                        Finish=interval.right_value,
                        Interval=str(interval)
                    )
                )
                if i == 0:
                    left_value, left_text = interval.left_value, interval.left_value

                if i == len(self) - 1:
                    right_value, right_text = interval.right_value, interval.right_value

        colors = generate_colors(len(self))
        fig = ff.create_gantt(
            data,
            colors=dict(zip([str(interval) for interval in self], colors)),
            index_col='Interval',
            group_tasks=True,
            height=250,
            title=f'Atomic interval {str(self)}',
            showgrid_x=True,
            bar_width=0.5
        )

        annotations = [
            dict(x=(d['Start'] + d['Finish']) / 2, y=0, text=d['Interval'], showarrow=False, font=dict(color='black'))
            for d in data
        ]
        fig['layout']['annotations'] = annotations

        # todo: xaxis type
        tick_values = list(round(x) for x in np.linspace(left_value, right_value, 10))
        tick_text = tick_values.copy()
        tick_text[0] = left_text
        tick_text[-1] = right_text

        fig.update_layout(
            xaxis_type='linear',
            xaxis=dict(
                tickmode='array',
                tickvals=tick_values,
                ticktext=tick_text,
            ),
            yaxis_visible=False,
        )
        return fig
