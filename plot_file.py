#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pathlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# FUNCTIONS
def make_plot_function(
    x_data,
    y_data,
    x_label,
    y_label,
    main_label,
    data_file,
    plot_subtitle,
    plot_file_path,
    sub_label,
    sub_y_data,
):
    """Function that creates and saves plots.

    Args:
        x_data (list): data for X axis
        y_data (list): data for Y axis
        x_label (str): label of X axis
        y_label (str): label of Y axis
        main_label (str): main plot legend label
        data_file (str): name of file with data
        plot_subtitle (str): plot subtitle
        plot_file_path (str): save path ending with plot name
        sub_label (str): legend label of sub_y_data fit
        sub_y_data (list): fitting data in DAE method
    """
    try:
        plt.scatter(x_data, y_data, label=main_label)
        if main_label:
            plt.legend()
        if sub_label:
            plt.plot(x_data, sub_y_data, label=sub_label)
            plt.legend()
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(data_file, {"horizontalalignment": "center"})
        plt.suptitle(plot_subtitle)
        plt.savefig(plot_file_path, dpi=300)
    except OSError:
        print("! OSERROR: Plot ", data_file + ".png couldn't be saved !")
    finally:
        plt.close()


def make_plot_call(
    data,
    loaded_files,
    data_dae,
    data_arrhenius,
    r2_table,
    list_p_optimal,
    column_t_name,
    column_r_name,
    save_directory,
    list_dae_r2_score,
    list_dae_regress,
    list_arr_params,
):
    """Function that makes passes data to make_plot_fuinction.

    Args:
        data (list): list of DataFrames of raw data
        loaded_files (list): list of names of files imported to program
        data_dae (list): list of DataFrames of calculted data
        data_arrhenius (list): list of DataFrames with calculated data for each impoted file
        r2_table (pandas.DataFrame): table of R^2 (cube of pearson coeficient) values
        list_p_optimal (list): list of tuples of optimal parameters 'a' and 'b' in a*X^b fit
        column_t_name (str): name of column containing temperature data
        column_r_name (str): name of column containing resistance data
        save_directory (str): directory of saved files
        list_dae_r2_score (list): list of R^2 values of fitting a*X^b
        list_dae_regress (list): list of tuples of best fitting parameters of linear
            reggresion with R^2 parameter
        list_arr_params (list): list of tuples of final calculated values in Arrhenius method
            (p, T0, R0)
    """
    save_directory += "/Plots"
    pathlib.Path(save_directory).mkdir(parents=True, exist_ok=True)
    for count, item in enumerate(loaded_files):
        pathlib.Path(save_directory + "/" + item).mkdir(parents=True, exist_ok=True)
    print("\nPlots saved:")
    file_count = 0

    # Plot R^2(p) from Arrhenius
    x_data = r2_table.iloc[:, 0]
    for count, item in enumerate(loaded_files, 1):
        y_data = r2_table.iloc[:, count]
        file_path = save_directory + "/" + item + "/r2_arr_" + item + ".png"
        make_plot_function(
            x_data,
            y_data,
            "p",
            "R$^{2}$",
            None,
            item,
            "Arrhenius R$^{2}$(p)",
            file_path,
            None,
            None,
        )
        file_count += 1
        print(file_count, file_path)

    # Plot raw data R(T)
    for count, item in enumerate(loaded_files, 0):
        temporary_data = data[count]
        x_data = temporary_data[column_t_name]
        y_data = temporary_data[column_r_name]
        file_path = save_directory + "/" + item + "/RT_raw" + item + ".png"
        make_plot_function(
            x_data,
            y_data,
            "T [Kelvin]",
            "R [Ohm]",
            None,
            item,
            "R(T)",
            file_path,
            None,
            None,
        )
        file_count += 1
        print(file_count, file_path)

    # Plot raw data R(T) with Arrhenius fit
    for count, item in enumerate(loaded_files, 0):
        temporary_data = data_arrhenius[count]
        optimal_params = list_arr_params[count]
        x_data = temporary_data[column_t_name]
        y_data = temporary_data[column_r_name]
        y_fit = temporary_data["R(T) fit"]
        p_param, t0_param, r0_param = tuple(optimal_params)
        sub_label = "fit R(T): p={}, T$_0$={:.2e}, R$_0$={:.2e}".format(
            p_param, t0_param, r0_param
        )
        file_path = save_directory + "/" + item + "/RT_fit" + item + ".png"
        make_plot_function(
            x_data,
            y_data,
            "T [Kelvin]",
            "R [Ohm]",
            None,
            item,
            "R(T)",
            file_path,
            sub_label,
            y_fit,
        )
        file_count += 1
        print(file_count, file_path)

    # Plot DAE(T)
    for count, item in enumerate(loaded_files, 0):
        temporary_data = data_dae[count]
        optimal_params = list_p_optimal[count]
        r2_score = list_dae_r2_score[count]
        x_data = temporary_data[column_t_name]
        y_data = temporary_data["DAE"]
        y_fit = temporary_data["aX^b fit"]
        a_param, b_param = tuple(optimal_params)
        sub_label = "fit aX$^b$: a={:.2e}, b={:.2e}".format(a_param, b_param)
        sub_label += ", R$^2$=%.3f" % r2_score
        file_path = save_directory + "/" + item + "/dae_fit_" + item + ".png"
        make_plot_function(
            x_data,
            y_data,
            "T [Kelvin]",
            "DAE [eV]",
            None,
            item,
            "DAE(T)",
            file_path,
            sub_label,
            y_fit,
        )
        file_count += 1
        print(file_count, file_path)

    # plot log(DAE)
    for count, item in enumerate(loaded_files, 0):
        temporary_data = data_dae[count]
        optimal_params = list_dae_regress[count]
        x_data = temporary_data["log(a) + b*log(T)"]
        y_data = temporary_data["log(DAE)"]
        y_fit = temporary_data["aX+b fit"]
        a_param, b_param, r2_param = tuple(optimal_params)
        sub_label = "fit aX+b: a={:.2e}, b={:.2e}, R$^2$={:.3f}".format(
            a_param, b_param, r2_param
        )
        file_path = save_directory + "/" + item + "/dae_log_fit_" + item + ".png"
        make_plot_function(
            x_data,
            y_data,
            "log(a) + b*log(T)",
            "log(DAE)",
            None,
            item,
            "log(DAE) = log(a) + b*log(T)",
            file_path,
            sub_label,
            y_fit,
        )
        file_count += 1
        print(file_count, file_path)


def simulate_r_t(
    simulate_t_min,
    simulate_t_max,
    simulate_t_step,
    simulate_r0_param,
    simulate_t0_param,
    simulate_p_param,
    save_directory,
):
    """Function for symulating data based on user's parameters

    Args:
        simulate_t_min (float): the lower limit of the range of temperature
        simulate_t_max (float): the higher limit of the range of temperature
        simulate_t_step (float): the step of temperature
        simulate_r0_param (float): value of R0 parameter
        simulate_t0_param (float): value of T0 parameter
        simulate_p_param (float): value of p parameter
        save_directory (str): directory of saved files
    """
    temperature_list = []
    for temperature in range(
        simulate_t_min, simulate_t_max + simulate_t_step, simulate_t_step
    ):
        temperature_list.append(temperature)
    simulate_data = pd.DataFrame(temperature_list, columns=["Temperature"])
    simulate_data["Resistance"] = simulate_r0_param * np.exp(1) ** (
        (simulate_t0_param / simulate_data["Temperature"]) ** simulate_p_param
    )

    main_label = "simulation: R$_0$={:.2e}, T$_0$={:.2e}, p={}".format(
        simulate_r0_param, simulate_t0_param, simulate_p_param
    )

    save_directory += "/Plots"
    pathlib.Path(save_directory).mkdir(parents=True, exist_ok=True)
    save_directory += "/simulation_R(T).png"

    print("Saving simulation plot R(T):\n0 ", save_directory)

    make_plot_function(
        simulate_data["Temperature"],
        simulate_data["Resistance"],
        "Temperature",
        "Resistance",
        main_label,
        "simulation",
        "R(T)",
        save_directory,
        None,
        None,
    )


if __name__ == "__main__":
    print("\nRun program 'index.py', insted of this one!\n")
