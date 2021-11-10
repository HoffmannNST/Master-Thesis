#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pathlib

# FUNCTIONS
def save_arrhenius(
    data_arrhenius,
    loaded_files,
    delimeter: str,
    decimal_separator: str,
    r2_table,
    save_directory,
):
    """Function that saves data calculated in calcualte_arrhenius function to .txt files.

    Args:
        data_arr (list): list of DataFrames of calculted data
        loaded_files (list): list of names of files imported to program
        delimeter (str): separator of columns in data file
        decimal_separator (str): decimal sign in numbers
        r2_table (pandas.DataFrame): table of R^2 (cube of pearson coeficient) values
        save_directory (str): directory of saved files
        list_arr_params (list): list of tuples of parameters calculated in
            arrhenius method for every datasets

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
        decimal=decimal_separator,
    )
    saved_files.append(save_directory + "/r2p_arr.txt")

    for count, item in enumerate(loaded_files, 0):
        temporary_data = data_arrhenius[count]
        data_path = save_directory + "/" + item + ".txt"
        temporary_data.to_csv(
            data_path, index=False, sep=delimeter, decimal=decimal_separator
        )
        saved_files.append(data_path)

    return saved_files


def save_summary_arrhenius(
    loaded_files,
    save_directory,
    list_arr_params,
):
    """Function that saves data calculated in calcualte_arrhenius function to .txt files.

    Args:
        loaded_files (list): list of names of files imported to program
        save_directory (str): directory of saved files
        list_arr_params (list): list of tuples of parameters calculated in
            arrhenius method for every datasets

    Returns:
        saved_files (list): list of saved files
    """
    saved_files = []

    save_directory += "/Arrhenius"
    pathlib.Path(save_directory).mkdir(parents=True, exist_ok=True)

    for count, item in enumerate(loaded_files, 0):
        data_path = save_directory + "/Arrhenius_summary.txt"
        file_append = open(data_path, "a")
        arr_params = list_arr_params[count]
        file_append.write("%s  <-- summary Arrhenius data" % item)
        file_append.write(
            "\nFinal calculated values p=%s, T0=%s, R0: %s\n\n*********************\n\n"
            % tuple(arr_params)
        )
        saved_files.append(data_path)

    return saved_files


def save_dae(
    data_dae,
    loaded_files,
    delimeter: str,
    decimal_separator: str,
    saved_files,
    save_directory,
):
    """Function that saves data calculated in calcualte_dae function to .txt files.

    Args:
        data_dae (list): list of DataFrames of calculted data
        loaded_files (list): list of names of files imported to program
        delimeter (str): separator of columns in data file
        decimal_separator (str): decimal sign in numbers
        saved_files (list): list of saved files
        list_p_optimal (list): list of tuples of optimal parameters 'a' and 'b' in a*X^b fit
        list_dae_r2_score (list): list of R^2 values of fitting a*X^b
        list_dae_regress (list): list of tuples of best fitting parameters of linear r
            eggresion with R^2 parameter
        list_dae_params (list): list of tuples of final calculated values in DAE method (p, T0)
        save_directory (str): directory for saving files

    Returns:
        saved_files (list): list of saved files
    """
    save_directory += "/DAE"
    pathlib.Path(save_directory).mkdir(parents=True, exist_ok=True)

    for count, item in enumerate(loaded_files, 0):
        temporary_data = data_dae[count]
        data_path = save_directory + "/" + item + ".txt"
        temporary_data.to_csv(
            data_path, index=False, sep=delimeter, decimal=decimal_separator
        )
        saved_files.append(data_path)

    print("\nFiles saved:")
    for count, item in enumerate(saved_files, 0):
        print(count + 1, item)
    return saved_files


def save_summary_dae(
    loaded_files,
    list_p_optimal,
    list_dae_r2_score,
    saved_files,
    list_dae_regress,
    list_dae_params_allometric,
    list_dae_params_log,
    save_directory,
):
    """Function that creates summary file with all DAE calculated data.

    Args:
        loaded_files (list): list of names of files imported to program
        list_p_optimal (list): list of tuples of optimal parameters 'a' and 'b' in a*X^b fit
        list_dae_r2_score (list): list of R^2 values of fitting a*X^b
        saved_files (list): list of saved files
        list_dae_regress (list): list of tuples of best fitting parameters of linear r
            eggresion with R^2 parameter
        list_dae_params_allometric (list): list of tuples of final calculated values
            in DAE method using allometric fit (p, T0)
        list_dae_params_log (list): list of tuples of final calculated values in DAE
            method using linear reggresion (p, T0)
        save_directory (str): directory for saving files


    Returns:
        saved_files (list): list of saved files
    """
    save_directory += "/DAE"
    pathlib.Path(save_directory).mkdir(parents=True, exist_ok=True)
    data_path = save_directory + "/DAE_summary.txt"
    for count, item in enumerate(loaded_files, 0):
        file_append = open(data_path, "a")

        p_optimal = list_p_optimal[count]
        dae_r2_score = list_dae_r2_score[count]
        dae_regress = list_dae_regress[count]
        dae_params_allometric = list_dae_params_allometric[count]
        dae_params_log = list_dae_params_log[count]
        file_append.write("%s  <-- summary DAE data" % item)
        file_append.write(
            "\nOptimal values of fitting a*X^b: a=%s, b=%s, " % tuple(p_optimal)
        )
        file_append.write("R^2: %s" % dae_r2_score)
        file_append.write(
            "\nOptimal values of linear reggresion for log(DAE) = b' + a'*log(T): a'=%s, b'=%s, R^2: %s"
            % tuple(dae_regress)
        )
        file_append.write(
            "\nFinal values calculated with allometric fit: p=%s, T0=%s"
            % tuple(dae_params_allometric)
        )
        file_append.write(
            "\nFinal values calculated with linear fit: p=%s, T0=%s\n\n*********************\n\n"
            % tuple(dae_params_log)
        )

        saved_files.append(data_path)

    print("\nFiles saved:")
    for count, item in enumerate(saved_files, 0):
        print(count + 1, item)
    return saved_files


if __name__ == "__main__":
    print("\nRun program 'index.py', insted of this one!\n")
