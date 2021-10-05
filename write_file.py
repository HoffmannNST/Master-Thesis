#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pathlib

# FUNCTIONS
def save_arrhenius(data_arrhenius, loaded_files, delimeter: str, coma: str, r2_table):
    """Function that saves data calculated in calcualte_arrhenius function to .txt files.

    Args:
        data_arr (list): list of DataFrames of calculted data
        loaded_files (list): list of names of files imported to program
        delimeter (str): separator of columns in data file
        coma (str): decimal sign in numbers
        r2_table (pandas.DataFrame): table of r^2 (cube of pearson coeficient) values

    Returns:
        list: list of saved files
    """
    x = -1
    saved_files = []

    pathlib.Path("Results/Arrhenius").mkdir(parents=True, exist_ok=True)

    r2_table.to_csv(
        "Results/Arrhenius/r2p_arr.txt", index=False, sep=delimeter, decimal=coma
    )
    saved_files.append("Results/Arrhenius/r2p_arr.txt")

    for i in loaded_files:
        x += 1
        temporary_data = data_arrhenius[x]
        data_path = "Results/Arrhenius/" + i + ".txt"
        temporary_data.to_csv(data_path, index=False, sep=delimeter, decimal=coma)
        saved_files.append(data_path)

    return saved_files


def save_dae(data_dae, loaded_files, delimeter: str, coma: str, saved_files):
    """Function that saves data calculated in calcualte_dae function to .txt files.

    Args:
        data_dae (list): list of DataFrames of calculted data
        loaded_files (list): list of names of files imported to program
        delimeter (str): separator of columns in data file
        coma (str): decimal sign in numbers
        saved_files (list): list of saved files

    Returns:
        saved_files (list): list of saved files
    """
    x = -1

    pathlib.Path("Results/DAE").mkdir(parents=True, exist_ok=True)

    for i in loaded_files:
        x += 1
        temporary_data = data_dae[x]
        data_path = "Results/DAE/" + i + ".txt"
        temporary_data.to_csv(data_path, index=False, sep=delimeter, decimal=coma)

        saved_files.append(data_path)

    # to be removed
    print("\nFiles saved:")
    for count, item in enumerate(saved_files, 0):
        print(count, item)
    return saved_files


if __name__ == "__main__":
    print("Run program 'index.py', insted of this one!")
