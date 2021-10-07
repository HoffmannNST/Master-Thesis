#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pandas as pd
import matplotlib.pyplot as plt
import pathlib

# FUNCTIONS
# Calculate
def make_plot(data, loaded_files, data_dae, r2_table, list_p_optimal):
    """Function that makes plots of 3 different functions and saves them as .png files.

    Args:
        data (list): list of DataFrames of raw data
        loaded_files (list): list of names of files imported to program
        data_dae (list): list of DataFrames of calculted data
        r2_table (pandas.DataFrame): table of r^2 (cube of pearson coeficient) values
        list_p_optimal (list): list of optimal parameters 'a' and 'b' in a*X^b fit
    """
    pathlib.Path("Results/Plots").mkdir(parents=True, exist_ok=True)
    print("\nPlots saved:")
    file_count = 0

    # Plot r^2(p)
    X = r2_table.iloc[:, 0]
    for count, item in enumerate(loaded_files, 1):
        try:
            Y = r2_table.iloc[:, count]
            plt.xlabel("p")
            plt.ylabel("r$^{2}$")
            plt.title(item, {"horizontalalignment": "center"})
            plt.suptitle("Arrhenius r$^{2}$(p)")
            plt.scatter(X, Y)
            file_path = "Results/Plots/r2_arr_" + item + ".png"
            plt.savefig(file_path, dpi=300)
            # plt.show()
            plt.close()
            file_count += 1
            print(file_count, file_path)
        except OSError:
            print("! ERROR: Plot ", item + ".png couldn't be saved !")
            plt.close()

    # Plot raw data R(T)
    for count, item in enumerate(loaded_files, 0):
        try:
            temporary_data = data[count]
            X = temporary_data.iloc[:, 0]
            Y = temporary_data.iloc[:, 1]
            plt.xlabel("T [Kelvin]")
            plt.ylabel("R [Ohm]")
            plt.title(item, {"horizontalalignment": "center"})
            plt.suptitle("R(T)")
            plt.scatter(X, Y)
            file_path = "Results/Plots/RT_" + item + ".png"
            plt.savefig(file_path, dpi=300)
            # plt.show()
            plt.close()
            file_count += 1
            print(file_count, file_path)
        except OSError:
            print("! ERROR: Plot ", item + ".png couldn't be saved !")
            plt.close()

    # Plot DAE(T)
    for count, item in enumerate(loaded_files, 0):
        try:
            temporary_data = data_dae[count]
            p_optimal = list_p_optimal[count]
            X = temporary_data.iloc[:, 0]
            Y = temporary_data.iloc[:, 4]
            Y_fit = temporary_data.iloc[:, 5]
            plt.xlabel("T [Kelvin]")
            plt.ylabel("DAE [eV]")
            plt.title(item, {"horizontalalignment": "center"})
            plt.suptitle("DAE(T)")
            plt.scatter(X, Y)
            plt.plot(X, Y_fit, label="fit aX^b: a=%5.4f, b=%5.4f" % tuple(p_optimal))
            plt.legend()
            file_path = "Results/Plots/DAE_" + item + ".png"
            plt.savefig(file_path, dpi=300)
            # plt.show()
            plt.close()
            file_count += 1
            print(file_count, file_path)
        except OSError:
            print("! ERROR: Plot ", item + ".png couldn't be saved !")
            plt.close()

    for count, item in enumerate(loaded_files, 0):
        try:
            temporary_data = data_dae[count]
            X_log = temporary_data["log(a) + b*log(T)"]
            Y_log = temporary_data["log(DAE)"]
            plt.scatter(X_log, Y_log)
            plt.xlabel("log(a) + b*log(T)")
            plt.ylabel("log(DAE)")
            plt.title(item, {"horizontalalignment": "center"})
            plt.suptitle("log(DAE) = log(a) + b*log(T)")
            file_path = "Results/Plots/DAE_log_fit_" + item + ".png"
            plt.savefig(file_path, dpi=300)
            plt.close()
            file_count += 1
            print(file_count, file_path)
        except OSError:
            print("! ERROR: Plot ", item + ".png couldn't be saved !")
            plt.close()


if __name__ == "__main__":
    print("Run program 'index.py', insted of this one!")
