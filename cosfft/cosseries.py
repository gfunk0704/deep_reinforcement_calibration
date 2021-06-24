from constant import I
from math import exp, log, pi
from model.sde import Sde
from nptyping import NDArray
from typing import Callable

import numpy as np

class CosSeries:
    __k = np.arange(0, 256, 1)

    def __init__(self, tau: float, sde: Sde) -> None:
        self.__expiry = tau
        self.__sde = sde

    def get_discount_factor(self) -> float:
        return self.__sde.get_yield_term_structure().discount_factor(self.__expiry)

    def get_expiry(self) -> float:
        return self.__expiry

    def get_sde(self) -> Sde:
        return self.__sde

    def get_put_price_calculator(self) -> Callable[[float], float]:
        integration_boundary = self.__sde.integration_boundary(self.__expiry)
        a, b = integration_boundary[0], integration_boundary[1]
        interval = b - a
        omega = self.__k * pi / interval
        psi = self.__sde.psi_levy(self.__expiry, omega)
        exp_term = lambda strike: np.exp(I * omega * (log(self.__sde.get_initial_value() / strike) - a))
        odd_coef = -a * omega
        exp_a = exp(a)
        odd_sin = np.sin(odd_coef)
        chi = (np.cos(odd_coef) - exp_a + omega * odd_sin) / (1 + omega * omega)
        phi = np.append(-a, odd_sin[1:] / omega[1:]) 
        u =  phi - chi
        u[0] *= 0.5
        return lambda strike: strike * 2 / interval * np.sum(np.real(psi * exp_term(strike) * u)) * self.get_discount_factor()
    
    @classmethod
    def set_n_grids(cls, n: int) -> None:
        cls.__k = np.arange(0, n, 1)

    @classmethod
    def get_n_grid(cls) -> int:
        return cls.__k.size

    