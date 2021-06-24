from timemanipulation.daycount import set_year_fraction
from timemanipulation.period import Period
from quotation.quote import Calendar, date, Quote

class InterestRateQuote(Quote):
    def __init__(self, value: float, tenor: Period, spot_lag: int, day_count: str, value_date: date, calendar: Calendar) -> None:
        super().__init__(value, value_date, calendar)
        self._year_fraction = set_year_fraction(day_count)
        self._fixing_date = self._calendar.next_n_businessday(value_date, spot_lag)
        self._expiry_date = self._calendar.convert_tenor_to_date(value_date, tenor)

    def expiry_date(self) -> date:
        return self._expiry_date
    

    
