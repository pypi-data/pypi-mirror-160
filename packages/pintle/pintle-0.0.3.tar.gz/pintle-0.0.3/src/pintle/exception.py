class AtomicIntervalException(Exception):
    pass


class AtomicIntervalWarning(Warning):
    pass


class IntervalsException(Exception):
    pass


class IntervalsWarning(Warning):
    pass


__all__ = [
    'AtomicIntervalException',
    'AtomicIntervalWarning',
    'IntervalsException',
    'IntervalsWarning',
]