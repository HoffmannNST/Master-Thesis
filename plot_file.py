#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pathlib
import matplotlib.pyplot as plt

# FUNCTIONS
def make_plot_function(
    x_data,
    y_data,
    x_label,
    y_label,
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
        data_file (str): name of file with data
        plot_subtitle (str): plot subtitle
        plot_file_path (str): save path ending with plot name
        sub_label (str): legend label of sub_y_data fit
        sub_y_data (list): fitting data in DAE method
    """
    try:
        plt.scatter(x_data, y_data)
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
    r2_table,
    list_p_optimal,
    column_t_name,
    column_r_name,
    save_directory,
    list_dae_r2_score,
):
    """Function that makes passes data to make_plot_fuinction.

    Args:
        data (list): list of DataFrames of raw data
        loaded_files (list): list of names of files imported to program
        data_dae (list): list of DataFrames of calculted data
        r2_table (pandas.DataFrame): table of R^2 (cube of pearson coeficient) values
        list_p_optimal (list): list of tuples of optimal parameters 'a' and 'b' in a*X^b fit
        column_t_name (str): name of column containing temperature data
        column_r_name (str): name of column containing resistance data
        save_directory (str): directory of saved files
        list_dae_r2_score (list): list of R^2 values of fitting a*X^b
    """
    save_directory += "/Plots"
    pathlib.Path(save_directory).mkdir(parents=True, exist_ok=True)
    print("\nPlots saved:")
    file_count = 0

    # Plot R^2(p) from Arrhenius
    x_data = r2_table.iloc[:, 0]
    for count, item in enumerate(loaded_files, 1):
        y_data = r2_table.iloc[:, count]
        file_path = save_directory + "/r2_arr_" + item + ".png"
        make_plot_function(
            x_data,
            y_data,
            "p",
            "R$^{2}$",
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
        file_path = save_directory + "/RT_" + item + ".png"
        make_plot_function(
            x_data, y_data, "T [Kelvin]", "R [Ohm]", item, "R(T)", file_path, None, None
        )
        file_count += 1
        print(file_count, file_path)

    # Plot DAE(T)
    for count, item in enumerate(loaded_files, 0):
        temporary_data = data_dae[count]
        p_optimal = list_p_optimal[count]
        r2_score = list_dae_r2_score[count]
        x_data = temporary_data[column_t_name]
        y_data = temporary_data["DAE"]
        y_fit = temporary_data["aX^b fit"]
        sub_label = "fit aX$^{b}$: a=%5.5f, b=%5.4f" % tuple(p_optimal)
        sub_label += ", R$^{2}$:%5.3f" % r2_score
        file_path = save_directory + "/dae_fit_" + item + ".png"
        make_plot_function(
            x_data,
            y_data,
            "T [Kelvin]",
            "DAE [eV]",
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
        x_data = temporary_data["log(a) + b*log(T)"]
        y_data = temporary_data["log(DAE)"]
        file_path = save_directory + "/dae_log_fit_" + item + ".png"
        make_plot_function(
            x_data,
            y_data,
            "log(a) + b*log(T)",
            "log(DAE)",
            item,
            "log(DAE) = log(a) + b*log(T)",
            file_path,
            None,
            None,
        )
        file_count += 1
        print(file_count, file_path)


if __name__ == "__main__":
    print("\nRun program 'index.py', insted of this one!\n")
