from datetime import date
from typing import Callable
from timemanipulation.daycount import set_year_fraction

class EvaluationEnvironment():
    def __init__(self, evaluation_date: date, day_count: str) -> None:
       self.set_evaluation_date(evaluation_date)
       self.set_day_count(day_count)

    def set_evaluation_date(self, evaluation_date: date) -> None:
        self.__evaluation_date = evaluation_date

    def get_evaluation_date(self) -> date:
        return self.__evaluation_date

    def set_day_count(self, day_count: str) -> None:
        self.__day_count = day_count
        self.__year_fraction = set_year_fraction(day_count)

    def get_day_count(self) -> str:
        return self.__day_count

    def get_year_fraction(self) -> Callable[[date, date], float]:
        return self.__year_fraction

    def maturity_years(self, expiry: date) -> float:
        return self.__year_fraction(self.__evaluation_date, expiry)

    
