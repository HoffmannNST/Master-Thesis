#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pathlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats, constants
from calculate_file import fit_linear, fit_dae

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
    sub_x_data,
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
            plt.plot(sub_x_data, sub_y_data, label=sub_label)
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


def get_min_max(data_column):
    """Function that gets min and max values from a column

    Args:
        data_column (list): list of data in the column

    Returns:
        min_value (float): min value in the column
        max_value (float): max value in the column
    """
    min_index = data_column.idxmin()
    max_index = data_column.idxmax()
    min_value = data_column[min_index]
    max_value = data_column[max_index]

    return min_value, max_value


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

    Returns:
        plot_file_count (int): counter of all saved plots
    """
    save_directory += "/Plots"
    pathlib.Path(save_directory).mkdir(parents=True, exist_ok=True)
    for count, item in enumerate(loaded_files):
        pathlib.Path(save_directory + "/" + item).mkdir(parents=True, exist_ok=True)
    print("\nPlots saved:")
    plot_file_count = 0

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
            None,
        )
        plot_file_count += 1
        print(plot_file_count, file_path)

    # Plot raw data R(T)
    for count, item in enumerate(loaded_files, 0):
        temporary_data = data[count]
        x_data = temporary_data[column_t_name]
        y_data = temporary_data[column_r_name]
        file_path = save_directory + "/" + item + "/RT_raw_" + item + ".png"
        make_plot_function(
            x_data,
            y_data,
            "Temperature [K]",
            "Resistance [$\Omega$]",
            None,
            item,
            "R(T)",
            file_path,
            None,
            None,
            None,
        )
        plot_file_count += 1
        print(plot_file_count, file_path)

    # Plot raw data R(T) with Arrhenius fit
    for count, item in enumerate(loaded_files, 0):
        temporary_data = data_arrhenius[count]
        optimal_params = list_arr_params[count]
        p_param, t0_param, r0_param = tuple(optimal_params)
        x_data = temporary_data[column_t_name]
        y_data = temporary_data[column_r_name]

        min_t_value, max_t_value = get_min_max(x_data)
        x_fit_range = np.linspace(min_t_value, max_t_value, 100)
        y_fit = r0_param * np.exp(1) ** ((t0_param / x_fit_range) ** p_param)

        sub_label = "fit R(T): p={}, T$_0$={:.2e}, R$_0$={:.2e}".format(
            p_param, t0_param, r0_param
        )
        file_path = save_directory + "/" + item + "/RT_fit_" + item + ".png"
        make_plot_function(
            x_data,
            y_data,
            "Temperature [K]",
            "Resistance [$\Omega$]",
            None,
            item,
            "R(T)",
            file_path,
            sub_label,
            x_fit_range,
            y_fit,
        )
        plot_file_count += 1
        print(plot_file_count, file_path)

    # Plot DAE(T)
    for count, item in enumerate(loaded_files, 0):
        temporary_data = data_dae[count]
        optimal_params = list_p_optimal[count]
        a_param, b_param = tuple(optimal_params)
        r2_score = list_dae_r2_score[count]
        x_data = temporary_data[column_t_name]
        y_data = temporary_data["DAE"]
        min_t_value, max_t_value = get_min_max(x_data)
        x_fit_range = np.linspace(min_t_value, max_t_value, 100)
        y_fit = fit_dae(x_fit_range, *optimal_params)
        sub_label = "fit aX$^b$: a={:.2e}, b={:.2e}".format(a_param, b_param)
        sub_label += ", R$^2$=%.3f" % r2_score
        file_path = save_directory + "/" + item + "/dae_fit_" + item + ".png"
        make_plot_function(
            x_data,
            y_data,
            "Temperature [K]",
            "DAE [eV]",
            None,
            item,
            "DAE(T)",
            file_path,
            sub_label,
            x_fit_range,
            y_fit,
        )
        plot_file_count += 1
        print(plot_file_count, file_path)

    # Plot DAE(T) with Arrhenius fit
    kb_const = constants.value("Boltzmann constant in eV/K")
    for count, item in enumerate(loaded_files, 0):
        temporary_data = data_dae[count]
        optimal_params = list_arr_params[count]
        p_param, t0_param, _ = tuple(optimal_params)
        x_data = temporary_data[column_t_name]
        y_data = temporary_data["DAE"]
        min_t_value, max_t_value = get_min_max(x_data)
        x_fit_range = np.linspace(min_t_value, max_t_value, 100)
        y_fit = (p_param * kb_const * (t0_param ** p_param)) * (
            x_fit_range ** (1 - p_param)
        )
        sub_label = "fit from Arrhenius: p={}, T$_0$={:.2e}".format(p_param, t0_param)
        file_path = save_directory + "/" + item + "/dae_fit_arr_" + item + ".png"
        make_plot_function(
            x_data,
            y_data,
            "Temperature [K]",
            "DAE [eV]",
            None,
            item,
            "DAE(T) fit with p, T$_{0}$ from Arrhenius",
            file_path,
            sub_label,
            x_fit_range,
            y_fit,
        )
        plot_file_count += 1
        print(plot_file_count, file_path)

    # plot log(DAE)
    for count, item in enumerate(loaded_files, 0):
        temporary_data = data_dae[count]
        optimal_params = list_dae_regress[count]
        x_data = temporary_data["log(T)"]
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
            "log(T)",
            "log(DAE)",
            None,
            item,
            "log(DAE) = b' + a'*log(T)",
            file_path,
            sub_label,
            x_data,
            y_fit,
        )
        plot_file_count += 1
        print(plot_file_count, file_path)

    return plot_file_count


# Plot muliple theoretical DAE(T) for different theoretical p values
def plot_theoretical_arrhenius(
    loaded_files,
    data_dae,
    column_t_name,
    theoretical_p_list,
    arr_theoretical_params_list,
    save_directory,
    plot_file_count,
):
    """Function that plots DAE curves for all theoretical p parameters with DAE(T)

    Args:
        loaded_files (list): list of names of files imported to program
        data_dae (list): list of DataFrames of calculted data
        column_t_name (str): name of column containing temperature data
        theoretical_p_list (list): list of theoretical p parameter to calculate r^2, T0, R0 from
        arr_theoretical_params_list (list): list of list of tuples with p and
            calculated r^2, T0, R0 parameters
        save_directory (str): directory of saved files
        plot_file_count (int): counter of all saved plots

    Returns:
        plot_file_count (int): counter of all saved plots
    """
    kb_const = constants.value("Boltzmann constant in eV/K")
    for count, item in enumerate(loaded_files, 0):
        temporary_data = data_dae[count]
        arr_theoretical_params_list2 = arr_theoretical_params_list[count]
        file_path = save_directory + "/Plots"
        x_data = temporary_data[column_t_name]
        y_data = temporary_data["DAE"]
        plt.xlabel("Temperature [K]")
        plt.ylabel("DAE [eV]")
        plt.title(
            item,
            {"horizontalalignment": "center"},
        )
        plt.suptitle("DAE(T) with Arrhenius  p, T$_0$ values fit")
        plt.scatter(x_data, y_data)
        for count2, _ in enumerate(theoretical_p_list):
            arr_theoretical_params_tuple = arr_theoretical_params_list2[count2]
            p_param, _, t0_param, __ = tuple(arr_theoretical_params_tuple)
            y_fit = (p_param * kb_const * (t0_param ** p_param)) * (
                temporary_data[column_t_name] ** (1 - p_param)
            )
            sub_label = "p={:.2f}, T$_0$={:.2e}".format(p_param, t0_param)
            plt.plot(x_data, y_fit, label=sub_label)

        pathlib.Path(file_path).mkdir(parents=True, exist_ok=True)
        file_path += "/" + item + "/dae_fit_theoretical_" + item + ".png"
        plt.legend()  # loc="upper right", fontsize="x-small"
        try:
            plt.savefig(file_path, dpi=300)
        except OSError:
            print(
                "! OSERROR: Plot dae_fit_theoretical_"
                + item
                + ".png couldn't be saved !"
            )
        finally:
            plt.close()

        plot_file_count += 1
        print(plot_file_count, file_path)
    return plot_file_count


# Plot multiple Arrhenius curves
def plot_arrhenius(
    data_arrhenius,
    loaded_files,
    list_arr_params,
    plot_file_count,
    save_directory,
):
    """Function that plots all the Arrhenius plots together

    Args:
        data_arrhenius (list): list of DataFrames with calculated data for each impoted file
        loaded_files (list): list of names of files imported to program
        list_arr_params (list): list of tuples of final calculated values in Arrhenius method
            (p, T0, R0)
        plot_file_count (int): counter of all saved plots
        save_directory (str): directory of saved files

    Returns:
        plot_file_count (int): counter of all saved plots
    """
    plt.xlabel("T$^{-p}$")
    plt.ylabel("ln(R$^{-1}$)")
    plt.title("Arrhenius best fits", {"horizontalalignment": "center"})
    for count, item in enumerate(loaded_files, 0):
        temporary_data = data_arrhenius[count]
        arr_params = list_arr_params[count]
        p_arr_param, _, __ = tuple(arr_params)
        column_p_name = "1/T^(" + str(round(p_arr_param, 3)) + ")"
        x_data = temporary_data[column_p_name]
        y_data = temporary_data["Ln(1/R)"]
        sub_label = "%s, p=%s" % (item, p_arr_param)
        plt.scatter(x_data, y_data, label=sub_label)

        slope, intercept, _, __, ___ = stats.linregress(x_data, y_data)
        y_fit = fit_linear(x_data, slope, intercept)
        plt.plot(x_data, y_fit)

    save_directory += "/Plots"
    pathlib.Path(save_directory).mkdir(parents=True, exist_ok=True)
    save_directory += "/Arrhenius_plots.png"
    plt.legend()
    try:
        plt.savefig(save_directory, dpi=300)
    except OSError:
        print("! OSERROR: Plot Arrhenius_plots.png couldn't be saved !")
    finally:
        plt.close()

    plot_file_count += 1
    print(plot_file_count, save_directory)
    return plot_file_count


# Plot raw data R(T)
def plot_r_t(
    loaded_files, column_t_name, column_r_name, data, save_directory, plot_file_count
):
    """Function that plots all R(T) raw data together

    Args:
        loaded_files (list): list of names of files imported to program
        column_t_name (str): name of column containing temperature data
        column_r_name (str): name of column containing resistance data
        data (list): list of DataFrames of raw data
        plot_file_count (int): counter of all saved plots
        save_directory (str): directory of saved files

    Returns:
        plot_file_count (int): counter of all saved plots
    """
    plt.xlabel("Temperature [K]")
    plt.ylabel("Resistance [$\Omega$]")
    plt.title("R(T)", {"horizontalalignment": "center"})
    for count, item in enumerate(loaded_files, 0):
        temporary_data = data[count]
        x_data = temporary_data[column_t_name]
        y_data = temporary_data[column_r_name]
        sub_label = "%s" % item
        plt.scatter(x_data, y_data, label=sub_label)

    save_directory += "/Plots"
    pathlib.Path(save_directory).mkdir(parents=True, exist_ok=True)
    save_directory += "/R(T)_plots.png"
    plt.legend()
    try:
        plt.savefig(save_directory, dpi=300)
    except OSError:
        print("! OSERROR: Plot R(T)_plots.png couldn't be saved !")
    finally:
        plt.close()

    plot_file_count += 1
    print(plot_file_count, save_directory)
    return plot_file_count


# Plot multiple R^2(p)
def plot_r2_p(r2_table, loaded_files, save_directory, plot_file_count):
    """Function that plots all R^2(p) together

    Args:
        r2_table (pandas.DataFrame): table of R^2 (cube of pearson coeficient) values
        loaded_files (list): list of names of files imported to program
        save_directory (str): directory of saved files
        plot_file_count (int): counter of all saved plots

    Returns:
        plot_file_count (int): counter of all saved plots
    """
    plt.xlabel("p")
    plt.ylabel("R$^{2}$")
    plt.title("Arrhenius R$^{2}$(p)", {"horizontalalignment": "center"})

    x_data = r2_table.iloc[:, 0]
    for count, item in enumerate(loaded_files, 1):
        y_data = r2_table.iloc[:, count]
        sub_label = "%s" % item
        plt.scatter(x_data, y_data, label=sub_label)

    save_directory += "/Plots"
    pathlib.Path(save_directory).mkdir(parents=True, exist_ok=True)
    save_directory += "/r2_p_arr.png"
    plt.legend()

    try:
        plt.savefig(save_directory, dpi=300)
    except OSError:
        print("! OSERROR: Plot r2_p_arr.png couldn't be saved !")
    finally:
        plt.close()

    plot_file_count += 1
    print(plot_file_count, save_directory)
    return plot_file_count


# Plot multiple DAE(T)
def plot_dae(loaded_files, data_dae, column_t_name, save_directory, plot_file_count):
    """Function that plots all DAE(T) plots together

    Args:
        loaded_files (list): list of names of files imported to program
        data_dae (list): list of DataFrames of calculted data
        column_t_name (str): name of column containing temperature data
        save_directory (str): directory of saved files
        plot_file_count (int): counter of all saved plots

    Returns:
        plot_file_count (int): counter of all saved plots
    """
    plt.xlabel("Temperature [K]")
    plt.ylabel("DAE [eV]")
    plt.title("DAE(T)", {"horizontalalignment": "center"})

    for count, item in enumerate(loaded_files, 0):
        temporary_data = data_dae[count]
        x_data = temporary_data[column_t_name]
        y_data = temporary_data["DAE"]
        sub_label = "%s" % item
        plt.scatter(x_data, y_data, label=sub_label)

    save_directory += "/Plots"
    pathlib.Path(save_directory).mkdir(parents=True, exist_ok=True)
    save_directory += "/dae_t.png"
    plt.legend()

    try:
        plt.savefig(save_directory, dpi=300)
    except OSError:
        print("! OSERROR: Plot dae_t.png couldn't be saved !")
    finally:
        plt.close()

    plot_file_count += 1
    print(plot_file_count, save_directory)
    return plot_file_count


def simulate_r_t(
    simulate_t_min,
    simulate_t_max,
    simulate_t_step,
    simulate_r0_param,
    simulate_t0_param,
    simulate_p_param,
    save_directory,
    plot_file_count,
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

    make_plot_function(
        simulate_data["Temperature"],
        simulate_data["Resistance"],
        "Temperature [K]",
        "Resistance [$\Omega$]",
        main_label,
        "simulation",
        "R(T)",
        save_directory,
        None,
        None,
        None,
    )

    plot_file_count += 1
    print(plot_file_count, save_directory)


if __name__ == "__main__":
    print("\nRun program 'index.py', insted of this one!\n")
