from constant import I
from termstructure.interestrate.yieldtermstructure import YieldTermStructure
from math import sqrt
from nptyping import NDArray
from typing import Dict, List, Tuple, Union
import abc
import numpy as np

class Sde(abc.ABC):
    def __init__(self, initial_value: float, yield_term_structure: YieldTermStructure) -> None:
        self.__initial_value = initial_value
        self.__yield_term_structure = yield_term_structure
        self.__par = np.zeros(self.n_parameter())
        
    def characteristic_functiondef (self, tau: float, omega: NDArray[float]) -> NDArray[complex]:
        return np.power(self.get_initial_value(), I * omega) * self.psi_levy(tau, omega)

    @abc.abstractmethod
    def _update_cf_parameter(self) -> None:
        return NotImplemented

    @abc.abstractmethod
    def parameter_name(self) -> List[str]:
        return NotImplemented

    @abc.abstractmethod
    def parameter_lower(self) -> List[float]:
        return NotImplemented

    @abc.abstractmethod
    def parameter_upper(self) -> List[float]:
        return NotImplemented

    @abc.abstractmethod
    def psi_levy(self, tau: float, omega: NDArray[float]) -> NDArray[complex]:
        return NotImplemented

    def n_parameter(self) -> int:
        return len(self.parameter_name())

    def set_initial_value(self, initial_value: float) -> None:
        self.__initial_value = initial_value

    def get_initial_value(self) -> float:
        return self.__initial_value

    def set_yield_term_structure(self, yield_term_structure: YieldTermStructure) -> None:
        self.__yield_term_structure = yield_term_structure

    def get_yield_term_structure(self) -> YieldTermStructure:
        return self.__yield_term_structure

    def get_parameter(self) -> Dict[str, float]:
        return dict(zip(self.parameter_name(), self.__par))

    def integration_boundary(self, tau: float) -> Tuple[float, float]:
        half_interval = 8 * sqrt(tau)
        return (-half_interval, half_interval)

    def set_parameter(self, par: Union[Dict[str, float], NDArray[float]]) -> None:
        if isinstance(par, np.ndarray):
            self.__par = par
        elif isinstance(par, dict):
            par_name = self.parameter_name()
            for i in range(self.n_parameter()):
                if par_name[i] in par:
                    self.__par[i] = par[par_name[i]]
        else:
            raise ValueError('par must be "Dict[str, float]" or "NDArray[float]"')
        self._update_cf_parameter()
            




    

    