import abc
from dataclasses import dataclass
from datetime import date, timedelta
from timemanipulation.dateutility import end_of_month, is_leap_year

@dataclass
class Period(abc.ABC):
    value: int

    def __str__(self) -> str:
        return str(self.value) + self.base()

    @abc.abstractmethod
    def base(self) -> str:
        return NotImplemented

    def __radd__(self, base_date: date) -> date:
        return (self + base_date)

class Days(Period):
    pass
    def base(self) -> str:
        return "D"

    def __add__(self, base_date: date) -> date:
        return base_date + timedelta(days = self.value)

    def __rsub__(self, base_date: date) -> date:
        return base_date + Days(-self.value)

class Weeks(Period):
    pass

    def base(self) -> str:
        return "D"

    def __add__(self, base_date: date) -> date:
        return base_date + timedelta(weeks = self.value)

    def __rsub__(self, base_date: date) -> date:
        return base_date + Weeks(-self.value)


class Months(Period):
    pass
    def base(self) -> str:
        return "M"

    def __add__(self, base_date: date) -> date:
        yyyy = base_date.year
        mm   = base_date.month + self.value
        dd   = base_date.day
        
        def shift_year(yyyy: int, mm: int, year_shift: int) -> int:
            while not (mm in range(1, 13)):
                yyyy += year_shift
                mm += year_shift 
            return yyyy, mm 

        if (mm > 12):
            yyyy, mm = shift_year(yyyy, mm, 1)
        elif (mm < 1):
            yyyy, mm = shift_year(yyyy, mm, -1)

        eom = end_of_month(yyyy, mm)
        dd = eom if (dd > eom) else dd
        return date(yyyy, mm, dd)

    def __rsub__(self, base_date: date) -> date:
        return base_date + Months(-self.value)

class Years(Period):
    pass
    def base(self) -> str:
        return "Y"

    def __add__(self, base_date:date)->date:
        yyyy = base_date.year + self.value
        dd = 28 if (not is_leap_year(yyyy)) and (base_date.month == 2) and (base_date.day == 29) else base_date.day
        return date(yyyy, base_date.month , dd)

    def __rsub__(self, base_date: date) -> date:
        return base_date + Years(-self.value)

def convert_string_to_period(tenor_str: str) -> Period:
    return {'D':Days, 'W':Weeks, 'M':Months, 'Y':Years}[tenor_str[-1].upper()](int(tenor_str[:-1]))