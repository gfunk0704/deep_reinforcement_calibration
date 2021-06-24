from datetime import date
from math import exp
from termstructure.interestrate.yieldtermstructure import YieldTermStructure
from typing import Union

class FlatYieldTermStructure(YieldTermStructure):
    def __init__(self, value_date: date, day_count: str) -> None:
        super().__init__(value_date, day_count)
        self.set_value(0)

    def set_value(self, value: float) -> None:
        self.__value = value

    def get_value(self) -> float:
        return self.__value

    def discount_factor(self, expiry: Union[float, date]) -> float:
        return exp(-self.__value * self._as_maturity_year(expiry))

    def inst_forward_rate(self, expiry: Union[float, date]) -> float:
        return self.__value

    def zero_rate(self, expiry: Union[float, date]) -> float:
        return self.__value