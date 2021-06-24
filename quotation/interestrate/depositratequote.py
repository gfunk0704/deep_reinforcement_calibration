from quotation.interestrate.interestratequote import Calendar, date, InterestRateQuote
from timemanipulation.period import Period

class DepositRateQuote(InterestRateQuote):
    def __init__(self, value: float, tenor: Period, spot_lag: int, day_count: str, value_date: date, calendar: Calendar) -> None:
        super().__init__(value, tenor, spot_lag, day_count, value_date, calendar)
        self.__tau = self._year_fraction(self._fixing_date, self._expiry_date)

    def calculation_period(self) -> float:
        return self.__tau
        
