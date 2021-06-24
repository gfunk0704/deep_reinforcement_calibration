from datetime import date
from evaluationenvironment import EvaluationEnvironment
from timemanipulation.calendar import Calendar

class PlainVanillaOption():
    def __init__(self, expiry_date: date, strike:float, option_type: str, premium: float, evaluation_envir: EvaluationEnvironment) -> None:
        self.__expiry = evaluation_envir.maturity_years(expiry_date)
        self.__strike = strike
        self.__option_type = option_type
        self.__premium = premium
        
    def get_strike(self) -> float:
        return self.__strike

    def get_expiry(self) -> float:
        return self.__expiry

    def get_option_type(self) -> str:
        return self.__option_type

    def get_premium(self) -> float:
        return self.__premium
    