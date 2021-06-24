from constant import SQRT_MACHINE_EPS
from dataclasses import dataclass
from nptyping import NDArray
from scipy.optimize import approx_fprime
from typing import Callable, List, Union
import nlopt
import numpy as np

@dataclass 
class OptimizationProblem:
    n: int
    obj_func: Callable[[NDArray[float]], float]
    lower_bound: List[float]
    upper_bound: List[float]

@dataclass
class OptimizationResult:
    message: int
    par: NDArray[float]
    value: float

    def __str__(self) -> str:
        return 'message: ' + self.message + '\n' + 'par: ' + str(self.par) + '\n' + 'value: ' + self.value + '\n'


class Optimizer:
    def __init__(self, problem: OptimizationProblem) -> None:
        self.__problem = problem
        self.__local_optimzer = self.__initialize_algo(nlopt.LN_BOBYQA)
        self.__global_optimizer = self.__initialize_algo(nlopt.GD_MLSL_LDS)
        self.__global_optimizer.set_local_optimizer(self.__local_optimzer)

    def optimize(self, initial_value: Union[NDArray[float], None] = None) -> OptimizationResult:
        if initial_value is None:
            initial_value = 0.5 * (np.array(self.__problem.upper_bound) + np.array(self.__problem.lower_bound))
        par = self.__global_optimizer.optimize(initial_value)
        return OptimizationResult(self.__global_optimizer.last_optimize_result(), par, self.__global_optimizer.last_optimum_value())

    def get_problem(self) -> OptimizationProblem:
        return self.__problem

    def __initialize_algo(self, algo_enum: int) -> nlopt.opt:
        algo = nlopt.opt(algo_enum, self.__problem.n)
        algo.set_min_objective(self.__set_nlopt_function(self.__problem.n, self.__problem.obj_func))
        algo.set_lower_bounds(self.__problem.lower_bound)
        algo.set_upper_bounds(self.__problem.upper_bound)
        algo.set_xtol_rel(SQRT_MACHINE_EPS)
        algo.set_ftol_rel(1e-10)
        return algo

    def __set_nlopt_function(self, n:int, func: Callable[[NDArray[float]], float]) -> Callable[[NDArray[float], NDArray[float]], float]:
        epsilon = np.array([SQRT_MACHINE_EPS] * n)
        gradient = lambda x: approx_fprime(x, func, epsilon)
        def nlopt_func(x: NDArray[float], grad: NDArray[float]) -> float:
            if grad.size > 0:
                grad[:] = gradient(x)
            return func(x)
        return nlopt_func

    
        
    
    
            

    
