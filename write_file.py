#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pathlib

# FUNCTIONS
def save_arrhenius(
    data_arrhenius, loaded_files, delimeter: str, coma: str, r2_table, save_directory
):
    """Function that saves data calculated in calcualte_arrhenius function to .txt files.

    Args:
        data_arr (list): list of DataFrames of calculted data
        loaded_files (list): list of names of files imported to program
        delimeter (str): separator of columns in data file
        coma (str): decimal sign in numbers
        r2_table (pandas.DataFrame): table of r^2 (cube of pearson coeficient) values
        save_directory (str): directory of saved files

    Returns:
        saved_files (list): list of saved files
    """
    saved_files = []

    save_directory += "/Arrhenius"
    pathlib.Path(save_directory).mkdir(parents=True, exist_ok=True)

    r2_table.to_csv(
        save_directory + "/r2p_arr.txt",
        index=False,
        sep=delimeter,
        decimal=coma,
    )
    saved_files.append(save_directory + "/r2p_arr.txt")

    for count, item in enumerate(loaded_files, 0):
        temporary_data = data_arrhenius[count]
        data_path = save_directory + "/" + item + ".txt"
        temporary_data.to_csv(data_path, index=False, sep=delimeter, decimal=coma)
        saved_files.append(data_path)

    return saved_files


def save_dae(
    data_dae,
    loaded_files,
    delimeter: str,
    coma: str,
    saved_files,
    list_p_optimal,
    list_DAE_r2_score,
    list_DAE_regress,
    save_directory,
):
    """Function that saves data calculated in calcualte_dae function to .txt files.

    Args:
        data_dae (list): list of DataFrames of calculted data
        loaded_files (list): list of names of files imported to program
        delimeter (str): separator of columns in data file
        coma (str): decimal sign in numbers
        saved_files (list): list of saved files
        save_directory (str): directory of saved files

    Returns:
        saved_files (list): list of saved files
    """
    save_directory += "/DAE"
    pathlib.Path(save_directory).mkdir(parents=True, exist_ok=True)

    for count, item in enumerate(loaded_files, 0):
        temporary_data = data_dae[count]
        p_optimal = list_p_optimal[count]
        DAE_r2_score = list_DAE_r2_score[count]
        data_path = save_directory + "/" + item + ".txt"
        temporary_data.to_csv(data_path, index=False, sep=delimeter, decimal=coma)
        file_append = open(data_path, "a")
        file_append.write(
            "\nOptimal values of fitting a*X^b: a=%s, b=%s, " % tuple(p_optimal)
        )
        file_append.write("R^2: %s" % DAE_r2_score)
        DAE_regress = list_DAE_regress[count]
        file_append.write(
            "\nOptimal values of linear reggresion for log(DAE) = log(a) + b*log(T): a'=%s, b'=%s, R^2: %s"
            % tuple(DAE_regress)
        )

        saved_files.append(data_path)

    # to be removed
    print("\nFiles saved:")
    for count, item in enumerate(saved_files, 0):
        print(count + 1, item)
    return saved_files


if __name__ == "__main__":
    print("\nRun program 'index.py', insted of this one!\n")
