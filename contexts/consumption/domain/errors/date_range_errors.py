from datetime import date

from contexts.consumption.domain.errors.domain_error import DomainError


class InvalidDateRangeError(DomainError):
    """Raised when a range of days ends before it begins."""

    def __init__(self, start: date, end: date) -> None:
        super().__init__(f"{start} comes after {end}")
        self.start = start
        self.end = end
