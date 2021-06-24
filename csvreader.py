from datetime import date
from evaluationenvironment import EvaluationEnvironment
from instrument.plainvanillaoption import PlainVanillaOption
from timemanipulation.dateutility import date_from_string
from typing import List, Union

import os
import pandas as pd

def raw_data_from_csv(file: str) -> pd.Series:
    raw_data = pd.read_csv(file, index_col='date')
    raw_data.index = pd.to_datetime(raw_data.index)
    return raw_data

def option_data_from_csv(value_date: date, eval_envir: EvaluationEnvironment) -> Union[List[PlainVanillaOption], None]:
    date_string = '{}-{}-{}'.format(value_date.year, value_date.month, value_date.day)
    file_name = 'pandas_option_' + date_string + '.csv'
    if file_name in os.listdir('./option_data/'):
        raw_data = pd.read_csv('./option_data/' + file_name)
        return list(raw_data.apply(lambda option_data: PlainVanillaOption(date_from_string(option_data['expiry']), float(option_data['strike']), option_data['type'],  float(option_data['close']), eval_envir),axis=1))
    else:
        return None
