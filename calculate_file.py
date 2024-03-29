#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
from math import exp
from scipy import stats, constants, optimize
from sklearn.metrics import r2_score
import pandas as pd
import numpy as np

# Predefined settings
data = []
data_arrenius = []
data_dae = []
list_Y_fit = []
list_p_optimal = []
list_dae_r2_score = []
list_dae_regress = []
list_arr_params = []
list_dae_params_allometric = []
list_dae_params_log = []

# FUNCTIONS
def p_steps_f(p_step, p_range_min, p_range_max):
    """Function that sets step for calculating parameter p in set range

    Returns:
        p_list (list): list of p parameter within set range with set step
    """
    p_list = []
    for count in np.arange(p_range_min + p_step, p_range_max + p_step, p_step):
        p_list.append(round(count, 3))

    return p_list


def fit_dae(x, a, b):
    """Function model for DAE nonlinear curve fitting with allometric function

    Args:
        x (float): Variable that we try to fit
        a (float): the directional factor
        b (float): exponent

    Returns:
        float: value passed to scipy.optimize.curve_fit
    """
    return a * x ** b


def fit_linear(x, a, b):
    """Function model for calculating linear fit

    Args:
        x (float): Variable that we try to fit
        a (float): the directional factor
        b (float): free element

    Returns:
        float: value of linear fit
    """
    return a * x + b


def calculate_arrhenius(
    data,
    loaded_files,
    p_list,
    p_step,
    column_t_name,
    column_r_name,
    p_range_min,
    p_range_max,
):
    """Function for calculating parameters p with Arrhenius curves.

    Args:
        data (list): list of DataFrames of raw data
        loaded_files (list): list of names of files imported to program
        p_list (list): list of p parameter within set range with set step
        p_step (float): increment of p parameter
        column_t_name (str): name of column containing temperature data
        column_r_name (str): name of column containing resistance data
        p_range_min (float): minimal value in range of fitting parameter p
        p_range_max (float): maximal value in range of fitting parameter p

    Returns:
        data_arrhenius (list): list of DataFrames with calculated data for each impoted file
        r2_table_arr (pandas.DataFrame): table of R^2 (cube of pearson coeficient) values
        list_arr_params (list): list of tuples of final calculated values in Arrhenius method
            (p, T0, R0)
    """
    data_arrhenius = list(data)

    # Tables of calculated parameters
    # r2 is a correlation coeficient
    r2_table_arrhenius = pd.DataFrame(p_list, columns=["p"])
    # T0 is a characteristic temp. deriviated from slope of function
    t0_table_arrhenius = pd.DataFrame(p_list, columns=["p"])
    # R0 is a pre-exponential factor deriviated from intercept of function
    r0_table_arrhenius = pd.DataFrame(p_list, columns=["p"])

    try:
        for count, item in enumerate(loaded_files, 0):
            temporary_data = data_arrhenius[count]
            new_data = temporary_data.loc[:, [column_t_name, column_r_name]]

            r2_list = []
            t0_list = []
            r0_list = []

            new_data["Ln(1/R)"] = np.log(1 / new_data[column_r_name])
            y_data = new_data["Ln(1/R)"]

            for p in np.arange(p_range_min + p_step, p_range_max + p_step, p_step):
                column_p_name = "1/T^(" + str(round(p, 3)) + ")"
                new_data[column_p_name] = 1 / (new_data[column_t_name] ** p)
                x_data = new_data[column_p_name]
                slope, intercept, r_value, _, __ = stats.linregress(x_data, y_data)
                # Do not calculate for p = 0 (because of division by 0)
                if p > -0.0001 and p < 0.0001:
                    r2_list.append(None)
                    t0_list.append(None)
                    r0_list.append(None)
                    continue
                r2_list.append(r_value ** 2)
                slope *= -1
                if slope > 0:
                    t0_list.append(slope ** (1 / p))
                else:
                    t0_list.append(np.NaN)
                r0_list.append(exp(-intercept))

            r2_table_arrhenius[item] = r2_list
            t0_table_arrhenius[item] = t0_list
            r0_table_arrhenius[item] = r0_list
            data_arrhenius[count] = new_data

        print("\nFROM ARRHENIUS METHOD:\nMax values of R^2(p):")
        for count, item in enumerate(loaded_files):
            index_p = r2_table_arrhenius[item].idxmax()
            max_r2 = r2_table_arrhenius.iloc[index_p, count + 1]
            arr_param_p = r2_table_arrhenius.iloc[index_p, 0]
            arr_param_t0 = t0_table_arrhenius.iloc[index_p, count + 1]
            arr_param_r0 = r0_table_arrhenius.iloc[index_p, count + 1]

            list_arr_params.append(tuple((arr_param_p, arr_param_t0, arr_param_r0)))

            print(
                "\t%s. max R^2 = %.4f for p = %s, parameters T0 = %s, R0 = %s, for data %s"
                % (count + 1, max_r2, arr_param_p, arr_param_t0, arr_param_r0, item)
            )

        for count, item in enumerate(loaded_files, 0):
            temporary_data = data_arrhenius[count]
            arr_params = list_arr_params[count]
            arr_param_p, arr_param_t0, arr_param_r0 = tuple(arr_params)
            temporary_data["R(T) fit"] = arr_param_r0 * np.exp(1) ** (
                (arr_param_t0 / temporary_data[column_t_name]) ** arr_param_p
            )
            data_arrhenius[count] = temporary_data

        return data_arrhenius, r2_table_arrhenius, list_arr_params

    except KeyError:
        print(
            "\n! KeyERROR: Check if decimal separator is set correctly or column indexes are correct !"
        )

    except TypeError:
        print("\n! TypeERROR: Check if decimal separator is set correctly !")

    except ValueError:
        print("\n! ValueERROR: Config file is incorrectly set or Data is incorrect !")

    except OverflowError:
        print("\n! OverflowERROR: Range of fitting parameter p is set incrroectly !")


# calculate r^2, T0, R0 parameters from theoretical p parameters
def theoretical_arrhenius(
    data_arrhenius,
    loaded_files,
    column_t_name,
    column_r_name,
    theoretical_p_list,
):
    """Function that calculates r^2, T0, R0 parameters for theoretical p values from user's input.

    Args:
        data_arrhenius (list): list of DataFrames with calculated data for each impoted file
        loaded_files (list): list of names of files imported to program
        column_t_name (str): name of column containing temperature data
        column_r_name (str): name of column containing resistance data
        theoretical_p_list (list): list of theoretical p parameter to calculate r^2, T0, R0 from

    Returns:
        arr_theoretical_params_list (list): list of list of tuples with p and
            calculated r^2, T0, R0 parameters
    """
    arr_theoretical_params_list = []

    for count, item in enumerate(loaded_files, 0):
        temporary_data = data_arrhenius[count]
        new_data = temporary_data.loc[:, [column_t_name, column_r_name]]

        arr_theoretical_params_tuples = []

        new_data["Ln(1/R)"] = np.log(1 / new_data[column_r_name])
        y_data = new_data["Ln(1/R)"]

        for p in theoretical_p_list:
            column_p_name = "1/T^(" + str(round(p, 3)) + ")"
            new_data[column_p_name] = 1 / (new_data[column_t_name] ** p)
            x_data = new_data[column_p_name]
            slope, intercept, r_value, _, __ = stats.linregress(x_data, y_data)
            # Do not calculate for p = 0 (because of division by 0)
            if p > -0.0001 and p < 0.0001:
                r2_param.append(None)
                t0_param.append(None)
                r0_param.append(None)
                continue
            slope *= -1
            if slope > 0:
                t0_param = slope ** (1 / p)
            else:
                t0_param = np.NaN
            r0_param = exp(-intercept)
            r2_param = r_value ** 2
            arr_theoretical_params_tuples.append(
                tuple((p, r2_param, t0_param, r0_param))
            )

        arr_theoretical_params_list.append(arr_theoretical_params_tuples)

    return arr_theoretical_params_list


def calculate_dae(data, loaded_files, column_t_name, column_r_name):
    """Function for calculating Differential Activation Energy (DAE).

    Args:
        data (list): list of DataFrames of raw data
        loaded_files (list): list of names of files imported to program
        column_t_name (str): name of column containing temperature data
        column_r_name (str): name of column containing resistance data

    Returns:
        data_dae (list): list of DataFrames with calculated data for each impoted file
        list_p_optimal (list): list of tuples of optimal parameters 'a' and 'b' in a*X^b fit
        list_dae_r2_score (list): list of R^2 values of fitting a*X^b
        list_dae_regress (list): list of tuples of best fitting parameters of linear
            reggresion with R^2 parameter
        list_dae_params_allometric (list): list of tuples of final calculated values
            in DAE method using allometric fit (p, T0)
        list_dae_params_log (list): list of tuples of final calculated values in DAE
            method using linear reggresion (p, T0)
    """
    data_dae = data
    # 'Boltzmann constant' or '...in eV/K' or '...in Hz/K' or '...in inverse meter per kelvin'
    kb_const = constants.value("Boltzmann constant in eV/K")

    print("\nFROM DAE METHOD: ")
    try:
        for count, item in enumerate(loaded_files, 0):
            temporary_data = data_dae[count]
            new_data = temporary_data.loc[:, [column_t_name, column_r_name]]
            new_data["(Kb*T)^(-1)"] = (new_data[column_t_name] * kb_const) ** (-1)
            new_data["(ln(R))"] = np.log(new_data[column_r_name])

            max_range = len(new_data[column_t_name]) - 2
            # Calculation of deriviative
            for j in range(0, max_range):
                j += 1
                new_data.loc[j, "DAE"] = 0.5 * (
                    (
                        (new_data.loc[j + 1, "(ln(R))"] - new_data.loc[j, "(ln(R))"])
                        / (
                            new_data.loc[j + 1, "(Kb*T)^(-1)"]
                            - new_data.loc[j, "(Kb*T)^(-1)"]
                        )
                    )
                    + (
                        (new_data.loc[j, "(ln(R))"] - new_data.loc[j - 1, "(ln(R))"])
                        / (
                            new_data.loc[j, "(Kb*T)^(-1)"]
                            - new_data.loc[j - 1, "(Kb*T)^(-1)"]
                        )
                    )
                )

            # First element
            new_data.loc[0, "DAE"] = (
                new_data.loc[1, "(ln(R))"] - new_data.loc[0, "(ln(R))"]
            ) / (new_data.loc[1, "(Kb*T)^(-1)"] - new_data.loc[0, "(Kb*T)^(-1)"])

            # Last element
            new_data.loc[max_range + 1, "DAE"] = (
                new_data.loc[max_range + 1, "(ln(R))"]
                - new_data.loc[max_range, "(ln(R))"]
            ) / (
                new_data.loc[max_range + 1, "(Kb*T)^(-1)"]
                - new_data.loc[max_range, "(Kb*T)^(-1)"]
            )

            x_data = new_data[column_t_name]
            y_data = new_data["DAE"]
            # DAE aX^b nonlinear regression fit
            p_optimal, _ = optimize.curve_fit(fit_dae, x_data, y_data)
            del _

            y_fit = fit_dae(x_data, *p_optimal)
            new_data["aX^b fit"] = y_fit

            list_p_optimal.append(p_optimal)
            dae_r2_score = r2_score(y_data, y_fit)
            list_dae_r2_score.append(dae_r2_score)

            # Linear regerssion fit
            new_data["log(DAE)"] = np.log10(new_data["DAE"])
            new_data["log(T)"] = np.log10(new_data[column_t_name])

            x_log = new_data["log(T)"]
            y_log = new_data["log(DAE)"]

            slope, intercept, r_value, _, __ = stats.linregress(x_log, y_log)

            y_fit = fit_linear(x_log, slope, intercept)
            new_data["aX+b fit"] = y_fit

            list_dae_regress.append(tuple((slope, intercept, r_value ** 2)))

            a_optimal_allometric, b_optimal_allometric = tuple(p_optimal)
            p_param_dae_allometric = 1 - b_optimal_allometric
            if p_param_dae_allometric > 0:
                t0_param_dae_allometric = a_optimal_allometric / (
                    p_param_dae_allometric * kb_const
                )
                t0_param_dae_allometric = t0_param_dae_allometric ** (
                    1 / p_param_dae_allometric
                )
            else:
                t0_param_dae_allometric = np.nan

            list_dae_params_allometric.append(
                tuple((p_param_dae_allometric, t0_param_dae_allometric))
            )

            p_param_dae_log = 1 - slope
            if p_param_dae_log > 0:
                t0_param_dae_log = (10 ** intercept) / (p_param_dae_log * kb_const)
                t0_param_dae_log = t0_param_dae_log ** (1 / p_param_dae_log)
            else:
                t0_param_dae_log = np.nan

            list_dae_params_log.append(tuple((p_param_dae_log, t0_param_dae_log)))

            print(str(count + 1), ". For data: " + item)
            print(
                "\tOptimal values of fitting a*X^b: \n\t\ta= %s, b= %s"
                % tuple(p_optimal)
            )
            print("\t\tR^2= ", dae_r2_score)

            print("\tLinear regression parameters for log(DAE) = b' + a'*log(T): ")
            print("\t\ta'= %s, b'= %s, R^2= %s" % (slope, intercept, (r_value ** 2)))

            print("\tFinal values calculated with allometric fit:")
            print(
                "\t\tp= %s, parameter T0= %s\n"
                % (p_param_dae_allometric, t0_param_dae_allometric)
            )

            print("\tFinal values calculated with linear fit:")
            print("\t\tp= %s, parameter T0= %s\n" % (p_param_dae_log, t0_param_dae_log))

            data_dae[count] = new_data
        return (
            data_dae,
            list_p_optimal,
            list_dae_r2_score,
            list_dae_regress,
            list_dae_params_allometric,
            list_dae_params_log,
        )

    except KeyError:
        print(
            "\n! ERROR: One or more data sets have different decimal separator than declared !"
        )


if __name__ == "__main__":
    print("\nRun program 'index.py', insted of this one!\n")
