from datetime import date
from quotation.interestrate.depositratequote import DepositRateQuote
from quotation.interestrate.interestratequote import InterestRateQuote
from timemanipulation.daycount import set_year_fraction
from typing import Union

import abc

class YieldTermStructure(abc.ABC):
    def __init__(self, value_date: date, day_count: str) -> None:
        self.__value_date = value_date
        self.__day_count = day_count
        self.__year_fraction = set_year_fraction(day_count)

    @abc.abstractmethod
    def discount_factor(self, expiry: Union[float, date]) -> float:
        return NotImplemented

    @abc.abstractmethod
    def inst_forward_rate(self, expiry: Union[float, date]) -> float:
        return NotImplemented

    @abc.abstractmethod
    def zero_rate(self, expiry: Union[float, date]) -> float:
        return NotImplemented

    def get_day_count(self) -> str:
        return self.__day_count

    def _as_maturity_year(self, expiry: Union[float, date]) -> float:
        return expiry if isinstance(expiry, float) else self.__year_fraction(self.__value_date, expiry)

    def implied_quote(self, quote: InterestRateQuote) -> float:
        if isinstance(quote, DepositRateQuote):
            return self.__deopsit_rate_implied_quote(quote)
        else:
            return ValueError('Unknown type of interest rate quote found')

    def __deopsit_rate_implied_quote(self, quote: DepositRateQuote) -> float:
        return (self.discount_factor(quote._fixing_date) / self.discount_factor(quote._expiry_date) - 1.0) / quote.calculation_period()


