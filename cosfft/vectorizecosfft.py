from constant import EMPTY_ARRAY
from cosfft.cosseries import CosSeries
from instrument.plainvanillaoption import PlainVanillaOption
from nptyping import NDArray

import numpy as np

class VectorizeCosFft():
    def __init__(self, cos_series: CosSeries) -> None:
        self.__cos_series = cos_series
        self.__strike = EMPTY_ARRAY
        self.__is_call = EMPTY_ARRAY
        self.__premium = EMPTY_ARRAY
    
    def append(self, option: PlainVanillaOption) -> None:
        if option.get_expiry() != self.__cos_series.get_expiry():
            raise Exception('tau mismatch')
        else:
            self.__strike = np.append(self.__strike, option.get_strike())
            self.__is_call = np.append(self.__is_call, option.get_option_type() == 'Call')
            self.__premium = np.append(self.__premium, option.get_premium())

    def get_option_price(self) -> NDArray[float]:
        discount_factor = self.__cos_series.get_discount_factor()
        calculator_put_price = self.__cos_series.get_put_price_calculator()
        put_price = np.array(list(map(calculator_put_price, self.__strike)))
        return np.where(self.__is_call, put_price + self.__cos_series.get_sde().get_initial_value() - self.__strike * discount_factor, put_price)

    def get_relative_error(self) -> NDArray[float]:
        return (self.get_option_price() - self.__premium)**2 / self.__premium
    