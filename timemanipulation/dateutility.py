from datetime import date

def is_leap_year(yyyy: int) -> int:
    return ((yyyy % 4 == 0 and yyyy % 100 != 0) or (yyyy % 400 == 0 and yyyy % 3200 != 0))

def date_from_string(date_str: str) -> date:
    str_list = date_str.split('/')
    return date(int(str_list[2]), int(str_list[0]), int(str_list[1]))

def end_of_month(yyyy: int, mm: int) -> int:
        if mm in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif mm in [4, 6, 9, 11]:
            return 30
        elif mm == 2:
            return 29 if is_leap_year(yyyy) else 28
        else:
            return None