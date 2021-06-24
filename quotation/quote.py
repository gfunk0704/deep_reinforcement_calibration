from dataclasses import dataclass
from timemanipulation.calendar import Calendar, date 
import abc

@dataclass
class Quote(abc.ABC):
    
    def __init__(self, value: float, value_date: date, calendar: Calendar) -> None:
        self._value = value  
        self._value_date = value_date 
        self._calendar = calendar

    def get_value(self) -> float:
        return self._value

    def set_value(self, value: float) -> None:
        self._value = value

    def get_value_date(self) -> date:
        return self._value_date

    def set_value_date(self, value_date: date) -> None:
        self._value = value_date

    @abc.abstractmethod
    def expiry_date(self) -> date:
        return NotImplemented
    
