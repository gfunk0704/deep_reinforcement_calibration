from constant import EMPTY_ARRAY
from cosfft.cosseries import CosSeries
from cosfft.vectorizecosfft import VectorizeCosFft
from instrument.plainvanillaoption import PlainVanillaOption
from nptyping import NDArray
from model.sde import Sde
from typing import Callable, List
import numpy as np

def set_object_function(sde: Sde, quote_col: List[PlainVanillaOption]) -> Callable[[NDArray[float]], float]:
    cos_fft_matrix = {}
    for quote in quote_col:
        expiry = quote.get_expiry()
        if expiry not in cos_fft_matrix:
            cos_fft_matrix[expiry] = VectorizeCosFft(CosSeries(expiry, sde))
        cos_fft_matrix[expiry].append(quote)
    cos_fft_matrix = list(cos_fft_matrix.values())

    def obj_func(par: NDArray[float]) -> float:
        sde.set_parameter(par)
        relative_error = EMPTY_ARRAY
        for vectorize_cos_fft in cos_fft_matrix:
            relative_error = np.append(relative_error, vectorize_cos_fft.get_relative_error())
        value = np.mean(relative_error)
        print(value)
        return value

    return obj_func