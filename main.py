
from calibration.objectfunction import set_object_function
from calibration.optimizer import OptimizationProblem, Optimizer
from csvreader import raw_data_from_csv, option_data_from_csv
from datetime import date, timedelta
from evaluationenvironment import EvaluationEnvironment
from model.bates import Bates
from quotation.interestrate.depositratequote import DepositRateQuote
from termstructure.interestrate.flatyieldtermstructure import FlatYieldTermStructure
from termstructure.interestrate.bootstrapping import bootstrap_yield_term_structure
from timemanipulation.countrycalendars.taiwan import taiwan_calendar
from timemanipulation.period import convert_string_to_period


def main() -> int:
    uderlying_list = raw_data_from_csv('underlying.csv')
    taibor_list = raw_data_from_csv('taibor.csv')
    eval_envir = EvaluationEnvironment(date(2021, 1, 1), 'ACT365FIXED')
    value_date = date(2021, 1, 4)
    while value_date <= date(2021, 1, 4):
        eval_envir.set_evaluation_date(value_date)
        option_col = option_data_from_csv(value_date, eval_envir)
        underlying = uderlying_list.loc[value_date]['close']
        taibor = taibor_list.loc[value_date]
        quote_col = []
        for tenor in ['1w', '2w' ,'1m', '2m', '3m', '6m', '9m', '1y']:
            quote_col.append(DepositRateQuote(taibor[tenor], convert_string_to_period(tenor), 2, 'ACT365FIXED', eval_envir.get_evaluation_date(), taiwan_calendar()))
        term_structure = bootstrap_yield_term_structure(FlatYieldTermStructure(eval_envir.get_evaluation_date(), eval_envir.get_day_count()), quote_col)
        model = Bates(underlying, term_structure)
        problem = OptimizationProblem(model.n_parameter(), set_object_function(model, option_col), model.parameter_lower(), model.parameter_upper())
        calibration_result = Optimizer(problem).optimize()
        print(calibration_result)
        value_date += timedelta(days=1)
    return 0

main()