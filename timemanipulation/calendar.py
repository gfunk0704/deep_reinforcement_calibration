from dataclasses import dataclass
from timemanipulation.period import Period, date, Days, end_of_month 
from typing import List


@dataclass
class Calendar:
    holiday_list: List[date]
    weekend_list: List[int]

    def is_holiday(self, target: date) -> bool:
        return True if (target.weekday() in self.weekend_list) else (target in self.holiday_list)

    def is_businessday(self, target: date) -> bool:
        return not self.is_holiday(target)

    def next_n_businessday(self, target: date, n: int) -> date:
        while (n > 0):
            target += Days(1)
            if (self.is_businessday(target)):
                n -=1
        return target

    def last_working_day_in_month(self, value_date: date) -> date:
        emo = date(value_date.year, value_date.month, end_of_month(value_date.year, value_date.month))
        while self.is_holiday(emo):
            emo -= Days(1)
        return emo

    def convert_tenor_to_date(self, value_date: date, tenor: Period) -> date:
        target = value_date + tenor
        if self.is_holiday(target):
            emo = self.last_working_day_in_month(target)
            if (tenor.base() in ["M", "Y"]) and (target > emo):
                return emo
            else:
                while self.is_holiday(target):
                    target += Days(1)
        return target

   

            