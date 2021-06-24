from timemanipulation.calendar import Calendar, date

__tw_national_holiday = [date(2021, 1, 1), date(2021, 2, 8), date(2021, 2, 9), date(2021, 2, 10),
                date(2021, 2, 11),date(2021, 2, 12), date(2021, 2, 15), date(2021, 2, 16),
                date(2021, 3, 1), date(2021, 4, 2),date(2021, 4, 5), date(2021, 4, 30),
                date(2021, 6, 14), date(2021, 9, 20),date(2021, 9, 21),date(2021, 10, 11),
                date(2021, 12, 31), date(2022,1,29), date(2022, 2, 1), date(2022, 2, 2),
                 date(2022, 2, 3), date(2022, 2, 4), date(2022, 2, 28)]

def taiwan_calendar() -> Calendar:
    holidays = __tw_national_holiday
    weekend = [5, 6]
    return Calendar(holidays, weekend)

def taiwan_taifex_calendar() -> Calendar:
    holidays = []
    holidays.extend(__tw_national_holiday)
    holidays.extend([date(2021, 2, 8), date(2021, 2, 9), date(2021, 2, 10)])
    weekend = [5, 6]
    return Calendar(holidays, weekend)

def as_common_era(public_era: str) -> date:
    sub_string = public_era.split('/')
    return date(int(sub_string[0]) + 1911, int(sub_string[1]), int(sub_string[2]))