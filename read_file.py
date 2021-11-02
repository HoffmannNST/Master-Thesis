#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pathlib
import yaml
import pandas as pd
from yaml.scanner import ScannerError

# Predefined settings
directories = []
loaded_files = []
data_names = []
data = []

# FUNCTIONS
def read_config():
    """Function that reads user's program settings from config.yml file.

    Returns:
        read_directory (string): directory of data files
        data_file_format (string): format of data files (e.g. '.txt')
        save_directory (str): directory for saving files
        delimeter (string): separator of columns in data file '/t' for tab
        decimal_separator (string): decimal sign in numbers: ',' or '.'
        column_t_index (str): index of column containing temperature data
        column_r_index (str): index of column containing resistance data
        p_range_min (float): minimal value in range of fitting parameter p
        p_range_max (float): maximal value in range of fitting parameter p
        p_step (float): increment of p parameter
    """

    try:
        with open("config.yml") as config_file:
            config_data = yaml.load(config_file, Loader=yaml.FullLoader)
    except FileNotFoundError:
        print("! FileNotFoundERROR: Config file does not work !")
    except ScannerError:
        print("! ScannerERROR: Config file does not work !")
        print(r"! Make sure to use / insted of \ !")

    read_directory = config_data["read_directory"]
    data_file_format = config_data["data_file_format"]
    save_directory = config_data["save_directory"]
    delimeter = config_data["delimeter"]
    decimal_separator = config_data["decimal_separator"]
    column_t_index = config_data["column_t_index"]
    column_r_index = config_data["column_r_index"]
    p_range_min = config_data["p_range_min"]
    p_range_max = config_data["p_range_max"]
    p_step = config_data["p_step"]

    return (
        read_directory,
        data_file_format,
        save_directory,
        delimeter,
        decimal_separator,
        column_t_index,
        column_r_index,
        p_range_min,
        p_range_max,
        p_step,
    )


def import_file(read_directory, data_file_format, delimeter, decimal_separator):
    """Function that imports data drom files in "Data" folder.

    Returns:
        data (list): list of DataFrames of raw data
        loaded_files (list): list of names of files imported to program
    """
    if pathlib.Path(read_directory).exists():
        directories_list = list(
            pathlib.Path(read_directory).glob("*" + data_file_format)
        )

        for item in directories_list:
            if pathlib.Path(item).exists():
                data.append(
                    pd.read_csv(
                        item, sep=delimeter, decimal=decimal_separator, header=0
                    )
                )
                loaded_files.append((item.name).split(".")[0])

        print("\nFiles loaded:")
        for count, item in enumerate(loaded_files, 0):
            print(count + 1, item + ".txt")
        return data, delimeter, decimal_separator, loaded_files

    else:
        input(
            "\nSpecified path '"
            + read_directory
            + "' does not exist!\nPress ENTER to continue...",
        )


def get_column_names(
    data,
    column_t_index,
    column_r_index,
):
    """Function that gets column indexes of T and R data in dataframe.

    Args:
        data (list): list of DataFrames of raw data
        column_t_index (str): index of column containing temperature data
        column_r_index (str): index of column containing resistance data

    Returns:
        column_t_name (str): name of column containing temperature data
        column_r_name (str): name of column containing resistance data
    """

    # Getting column names
    temp_data = data[0]
    data_names = temp_data.columns
    column_t_name = data_names[column_t_index]
    column_r_name = data_names[column_r_index]

    print('\nSelected columns: "' + column_t_name + '", "' + column_r_name + '"')

    return column_t_name, column_r_name


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
