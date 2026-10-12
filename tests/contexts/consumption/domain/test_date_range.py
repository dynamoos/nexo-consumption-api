from datetime import date

import pytest

from contexts.consumption.domain.errors.date_range_errors import InvalidDateRangeError
from contexts.consumption.domain.value_objects.date_range import DateRange


def test_a_range_may_span_many_days() -> None:
    days = DateRange(date(2026, 9, 1), date(2026, 9, 30))

    assert (days.start, days.end) == (date(2026, 9, 1), date(2026, 9, 30))


def test_a_range_may_be_a_single_day() -> None:
    day = date(2026, 9, 30)

    assert DateRange(day, day).start == day


def test_a_range_cannot_end_before_it_begins() -> None:
    with pytest.raises(InvalidDateRangeError) as refused:
        DateRange(date(2026, 9, 30), date(2026, 9, 1))

    assert refused.value.start == date(2026, 9, 30)
    assert refused.value.end == date(2026, 9, 1)
