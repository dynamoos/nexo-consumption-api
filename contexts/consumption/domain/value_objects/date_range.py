from dataclasses import dataclass
from datetime import date

from contexts.consumption.domain.errors.date_range_errors import (
    InvalidDateRangeError,
)


@dataclass(frozen=True)
class DateRange:
    """A span of whole days, both ends included."""

    start: date
    end: date

    def __post_init__(self) -> None:
        if self.start > self.end:
            raise InvalidDateRangeError(self.start, self.end)
