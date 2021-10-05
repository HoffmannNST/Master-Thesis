#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pandas as pd
import numpy as np
from math import exp
from scipy import stats, constants, optimize
from sklearn.metrics import r2_score

import matplotlib.pyplot as plt

# Predefined settings
data = []
data_arrenius = []
data_dae = []
list_Y_fit = []
list_p_optimal = []

# FUNCTIONS
def p_steps_F():
    """Function that sets step for calculating parameter p in range from 0 to 1

    Returns:
        p_list (list): list of p parameter within set range with set step
        p_step (float): increment of p parameter
    """
    try:
        # p_step = float(input('\nEnter the step for the p parameter (i.e. 0.1): '))
        p_step = 0.1
    except:
        print("Invalid input!")
        p_step = 0.1

    p_list = []
    for p in np.arange(0 + p_step, 1 + p_step, p_step):
        p_list.append(round(p, 3))
    return p_list, p_step


def DAE_fit(x, a, b):
    """Function model for DAE nonlinear curve fitting with allometric function

    Args:
        x (float): Variable that we try to fit
        a (float): the directional factor
        b (float): exponent

    Returns:
        float: value passed to scipy.optimize.curve_fit
    """
    return a * x ** b


def calculate_arrhenius(data, loaded_files, p_list, p_step):
    """Function for calculating parameters p with Arrhenius curves.

    Args:
        data (list): list of DataFrames of raw data
        loaded_files (list): list of names of files imported to program
        p_list (list): list of p parameter within set range with set step
        p_step (float): increment of p parameter

    Returns:
        data_arr (list): list of DataFrames with calculated data for each impoted file
        r2_table_arr (pandas.DataFrame): table of r^2 (cube of pearson coeficient) values
        p_list (list): list of p parameter within set range with set step
        p_step (float): increment of p parameter
    """
    x = -1
    data_arrhenius = list(data)

    # Tables of calculated parameters
    r2_table_arrhenius = pd.DataFrame(
        p_list, columns=["p"]
    )  # r2 is a correlation coeficient
    T0_table_arrhenius = pd.DataFrame(
        p_list, columns=["p"]
    )  # T0 is a characteristic temp. deriviated from slope of function
    R0_table_arrhenius = pd.DataFrame(
        p_list, columns=["p"]
    )  # R0 is a pre-exponential factor deriviated from intercept of function

    try:
        for i in loaded_files:
            x += 1

            temporary_data = data_arrhenius[x]
            new_data = temporary_data.loc[:, ["Temperatura [K]", "Opor"]]
            new_data["Ln(1/R)"] = np.log(1 / new_data["Opor"])

            Y = new_data["Ln(1/R)"]
            r2_list = []
            T0_list = []
            R0_list = []

            for p in np.arange(0 + p_step, 1 + p_step, p_step):
                column_p_name = "p = " + str(round(p, 3))
                new_data[column_p_name] = 1 / (new_data["Temperatura [K]"] ** p)
                X = new_data[column_p_name]
                slope, intercept, r_value, p_value, standard_error = stats.linregress(
                    X, Y
                )
                del p_value
                del standard_error
                r2_list.append(r_value ** 2)
                slope *= -1
                T0_list.append(slope ** (1 / p))
                R0_list.append(exp(-intercept))

            r2_table_arrhenius[i] = r2_list
            T0_table_arrhenius[i] = T0_list
            R0_table_arrhenius[i] = R0_list
            data_arrhenius[x] = new_data

        print("\nMax values of r^2(p):")
        for i, j in enumerate(loaded_files):
            index_p = r2_table_arrhenius[j].idxmax()
            max_r2 = r2_table_arrhenius.iloc[index_p, i + 1]
            param_p = r2_table_arrhenius.iloc[index_p, 0]
            param_T0 = T0_table_arrhenius.iloc[index_p, i + 1]
            param_R0 = R0_table_arrhenius.iloc[index_p, i + 1]
            print(
                "%s. max r^2 = %.3f for p = %.2f, parameters T0 = %.2f, R0 = %.2f, for data %s"
                % (i + 1, max_r2, param_p, param_T0, param_R0, j)
            )

        return data_arrhenius, r2_table_arrhenius, p_list, p_step

    except KeyError:
        print(
            "\n! ERROR: One or more data sets have different decimal separator then declared !"
        )


def calculate_dae(data, loaded_files):
    """Function for calculating Differential Activation Energy (DAE).

    Args:
        data (list): list of DataFrames of raw data
        loaded_files (list): list of names of files imported to program
        p_list (list): list of p parameter within set range with set step
        p_step (float): increment of p parameter

    Returns:
        data_dae (list): list of DataFrames with calculated data for each impoted file
        list_p_optimal (list): list of optimal parameters 'a' and 'b' in a*X^b fit
    """
    x = -1
    data_dae = data
    Kb = constants.value(
        "Boltzmann constant in eV/K"
    )  # 'Boltzmann constant' or '...in eV/K' or '...in Hz/K' or '...in inverse meter per kelvin'

    try:
        for i in loaded_files:
            x += 1
            temporary_data = data_dae[x]
            new_data = temporary_data.loc[:, ["Temperatura [K]", "Opor"]]
            new_data["(Kb*T)^(-1)"] = (new_data["Temperatura [K]"] * Kb) ** (-1)
            new_data["(Ln(R))"] = np.log(new_data["Opor"])

            max_range = len(new_data["Temperatura [K]"]) - 2
            # Calculation of deriviative
            for j in range(0, max_range):
                j += 1
                new_data.loc[j, "DAE"] = 0.5 * (
                    (
                        (new_data.loc[j + 1, "(Ln(R))"] - new_data.loc[j, "(Ln(R))"])
                        / (
                            new_data.loc[j + 1, "(Kb*T)^(-1)"]
                            - new_data.loc[j, "(Kb*T)^(-1)"]
                        )
                    )
                    + (
                        (new_data.loc[j, "(Ln(R))"] - new_data.loc[j - 1, "(Ln(R))"])
                        / (
                            new_data.loc[j, "(Kb*T)^(-1)"]
                            - new_data.loc[j - 1, "(Kb*T)^(-1)"]
                        )
                    )
                )

            new_data.loc[0, "DAE"] = (
                new_data.loc[1, "(Ln(R))"] - new_data.loc[0, "(Ln(R))"]
            ) / (new_data.loc[1, "(Kb*T)^(-1)"] - new_data.loc[0, "(Kb*T)^(-1)"])

            new_data.loc[max_range + 1, "DAE"] = (
                new_data.loc[max_range + 1, "(Ln(R))"]
                - new_data.loc[max_range, "(Ln(R))"]
            ) / (
                new_data.loc[max_range + 1, "(Kb*T)^(-1)"]
                - new_data.loc[max_range, "(Kb*T)^(-1)"]
            )

            X = new_data["Temperatura [K]"]
            Y = new_data["DAE"]

            p_optimal, p_covariance = optimize.curve_fit(DAE_fit, X, Y)
            del p_covariance

            Y_fit = DAE_fit(X, *p_optimal)
            new_data["aX^b fit"] = Y_fit
            print(new_data)

            list_p_optimal.append(p_optimal)

            print(
                "\nOptymalne wartości dopasowania a*X^b: a=%s, b=%s" % tuple(p_optimal)
            )
            print("R^2:", r2_score(Y, Y_fit), "\n")

            data_dae[x] = new_data

        return data_dae, list_p_optimal

    except KeyError:
        print(
            "\n! ERROR: One or more data sets have different decimal separator then declared !"
        )


if __name__ == "__main__":
    print("Run program 'index.py', insted of this one!")
