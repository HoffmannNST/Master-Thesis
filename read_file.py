#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pandas as pd
import pathlib

# Predefined settings
directories = []
loaded_files = []
data_names = []
data = []

# FUNCTIONS
def import_file():
    """Function that imports data drom files in "Data" folder.

    Returns:
        data (list): list of DataFrames of raw data
        delimeter (string): separator of columns in data file '/t' for tab
        coma (string): decimal sign in numbers: ',' or '.'
        loaded_files (list): list of names of files imported to program
    """

    directory = input("\nSpecify folder path (i.e. C:/Data): ")
    if directory == "":
        directory = "./Data"

    if pathlib.Path(directory).exists() == True:
        directories_list = list(pathlib.Path(directory).glob("*.txt"))

        delimeter = input("\nSpecify columns separator (i.e. symbols [, ; .] or tab): ")
        if delimeter in ("", "tab"):
            delimeter = "\t"

        coma = input("Specify decimal separator in the files: ")  # '.' or ','
        if coma == "":
            coma = ","

        for item in directories_list:
            if pathlib.Path(item).exists() == True:
                data.append(pd.read_csv(item, sep=delimeter, decimal=coma, header=0))
                loaded_files.append((item.name).split(".")[0])

        print("\nFiles loaded:")
        for count, item in enumerate(loaded_files, 0):
            print(count + 1, item + ".txt")
        return data, delimeter, coma, loaded_files

    else:
        input(
            "\nSpecified path '"
            + directory
            + "' does not exist!\nPress ENTER to continue...",
        )


def get_column_names(data):
    """Function that gets column indexes of T and R data in dataframe.

    Args:
        data (list): list of DataFrames of raw data

    Returns:
        T_column_name (str): name of column containing temperature data
        R_column_name (str): name of column containing resistance data
    """
    # Getting column indexes
    T_column_index = input("\nSpecify column index of temperature data: ")
    if T_column_index == "":
        T_column_index = 0
    else:
        T_column_index = int(T_column_index)
    R_column_index = input("Specify column index of resistance data: ")
    if R_column_index == "":
        R_column_index = 1
    else:
        R_column_index = int(T_column_index)

    # Getting column names
    temp_data = data[0]
    data_names = temp_data.columns
    T_column_name = data_names[T_column_index]
    R_column_name = data_names[R_column_index]

    print('\nSelected columns: "' + T_column_name + '", "' + R_column_name + '"')

    return T_column_name, R_column_name


def get_save_path():
    """Function that gets directory for saved files.

    Returns:
        save_directory (str): directory of saved files
    """
    save_directory = input("\nSpecify SAVE directory path (i.e. C:/Results): ")
    if save_directory == "":
        save_directory = "./Results"
    else:
        save_directory += "/Results"

    pathlib.Path(save_directory).mkdir(parents=True, exist_ok=True)

    return save_directory


if __name__ == "__main__":
    print("\nRun program 'index.py', insted of this one!\n")
