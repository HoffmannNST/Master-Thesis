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
    while True:
        # directory = 'Data' + input('\nSpecify folder path: Data/')
        directory = "Data"

        if pathlib.Path(directory).exists() == True:
            directories_list = list(pathlib.Path(directory).glob("*.txt"))

            # delimeter = input('\nSpecify columns separator (i.e. symbol [, ; .] or \t for tab):\n')     # /t - tab
            delimeter = "\t"
            # coma = input('\nSpecify decimal separator in the files:\n')     # '.' or ','
            coma = ","

            for i in directories_list:
                if pathlib.Path(i).exists() == True:
                    data.append(pd.read_csv(i, sep=delimeter, decimal=coma, header=0))
                    loaded_files.append((i.name).split(".")[0])

            print("\nFiles loaded:")
            for count, item in enumerate(loaded_files, 0):
                print(count, item + ".txt")
            return data, delimeter, coma, loaded_files

        else:
            input("\nSpecified path does not exist!\nPress ENTER to continue...")


if __name__ == "__main__":
    print("Run program 'index.py', insted of this one!")
