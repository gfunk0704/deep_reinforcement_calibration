from datetime import date
from typing import Callable

__days_in_year = {"ACT360": 360, "ACT365FIXED": 365}

def dt(day_count: str) -> float:
    return 1 / __days_in_year[day_count]

def set_year_fraction(day_count: str) -> Callable[[date, date], float]:
    dominator = __days_in_year[day_count]
    return lambda start_date, end_date: (end_date - start_date).days / dominator