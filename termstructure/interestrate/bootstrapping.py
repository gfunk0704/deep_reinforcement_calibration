from quotation.interestrate.interestratequote import InterestRateQuote
from scipy.optimize import minimize_scalar
from termstructure.interestrate.yieldtermstructure import YieldTermStructure
from termstructure.interestrate.flatyieldtermstructure import FlatYieldTermStructure
from typing import List
import numpy as np

def __bootstrap_flat_yield_term_structure(term_structure: FlatYieldTermStructure, quote_col: List[InterestRateQuote]) -> FlatYieldTermStructure:
    market_value = np.array(list(map(lambda quote: quote.get_value(), quote_col)))
    def obj_func(guess:float)->float:
        term_structure.set_value(guess)
        value_diff = (np.array(list(map(term_structure.implied_quote, quote_col))) - market_value)
        return np.mean(value_diff * value_diff / market_value) 
    optim_result = minimize_scalar(fun=obj_func, bounds=(-0.05, 0.5), method='brent')
    term_structure.set_value(optim_result['x'])
    return term_structure
    

def bootstrap_yield_term_structure(term_structure: YieldTermStructure, quote_col: List[InterestRateQuote]) -> YieldTermStructure:
    if isinstance(term_structure, FlatYieldTermStructure):
        return __bootstrap_flat_yield_term_structure(term_structure, quote_col)
    else:
        return ValueError('Unknown type of yield term structure')