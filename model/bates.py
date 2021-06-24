from constant import I, SQRT_MACHINE_EPS
from model.sde import Sde
from nptyping import NDArray
from typing import Dict, List
import numpy as np

class Bates(Sde):
    pass

    def _update_cf_parameter(self) -> None:
        par = self.get_parameter()
        self.__sigma_sqr = par['sigma'] * par['sigma']
        self.__b_coef = (par['kappa'] * par['theta']) / self.__sigma_sqr
        self.__c_coef = par['v0'] / self.__sigma_sqr
        self.__rho_sigma = par['rho'] * par['sigma']
        self.__lambda_mu_j = par['lambda'] * par['mu_j']
        self.__half_sigma_j_sqr = 0.5 * par['sigma_j']**2
        self.__kappa = par['kappa']
        self.__lambda = par['lambda']
        self.__mu_j = par['mu_j']

    def parameter_name(self) -> List[str]:
        return ['v0', 'kappa', 'theta', 'sigma', 'rho', 'lambda', 'mu_j', 'sigma_j']

    def parameter_lower(self) -> List[float]:
        return [SQRT_MACHINE_EPS, SQRT_MACHINE_EPS, SQRT_MACHINE_EPS, SQRT_MACHINE_EPS, -1, SQRT_MACHINE_EPS, -1, SQRT_MACHINE_EPS]

    def parameter_upper(self) -> List[float]:
        return [1, 3, 1, 1, 1, 10, 5, 5]

    def psi_levy(self, tau: float, omega: NDArray[float]) -> NDArray[complex]:
        self.__a_coef = self.get_yield_term_structure().zero_rate(tau) * tau
        i_omega = I * omega
        rho_sigma_i_omega = self.__rho_sigma * i_omega
        d_coef = self.__kappa - rho_sigma_i_omega
        d = np.sqrt(d_coef * d_coef + self.__sigma_sqr * (i_omega + omega * omega))
        g_numerator = d_coef - d
        g = g_numerator / (d_coef + d)
        exp_dt = np.exp(-d * tau)
        g_exp = 1 - g * exp_dt
        big_a = self.__a_coef * i_omega
        big_b = self.__b_coef * (g_numerator * tau - 2 * np.log(g_exp / (1 - g)))
        big_c = self.__c_coef * g_numerator * (1 - exp_dt) / g_exp
        big_d = -self.__lambda_mu_j * i_omega * tau + self.__lambda * tau * (np.exp(self.__mu_j * i_omega - self.__half_sigma_j_sqr * omega * omega) - 1)
        return np.exp(big_a + big_b + big_c + big_d)