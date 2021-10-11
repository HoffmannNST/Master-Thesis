#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import functions from additional files
from read_file import import_file, get_column_names, get_save_path
from calculate_file import calculate_arrhenius, calculate_dae, p_steps_F
from write_file import save_arrhenius, save_dae
from plot_file import make_plot

# START XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Welcome message
print("\nWelcome to program!")

# Import file
data, delimeter, coma, loaded_files = import_file()

# Select columns in dataframe
T_column_name, R_column_name = get_column_names(data)

# Choosing fitting range of p parameter
p_list, p_step = p_steps_F()

# Setting save folder
save_directory = get_save_path()

# Calculator Arrhenius
data_arrhenius, r2_table, p_list, p_step = calculate_arrhenius(
    data, loaded_files, p_list, p_step, T_column_name, R_column_name
)

# Save Arrhenius data
saved_files = save_arrhenius(
    data_arrhenius, loaded_files, delimeter, coma, r2_table, save_directory
)

# Calculator DAE
data_dae, list_p_optimal, list_DAE_r2_score, list_DAE_regress = calculate_dae(
    data, loaded_files, T_column_name, R_column_name
)

# Save DAE data
saved_files = save_dae(
    data_dae,
    loaded_files,
    delimeter,
    coma,
    saved_files,
    list_p_optimal,
    list_DAE_r2_score,
    list_DAE_regress,
    save_directory,
)

# Plot
make_plot(
    data,
    loaded_files,
    data_dae,
    r2_table,
    list_p_optimal,
    T_column_name,
    R_column_name,
    save_directory,
)

input("\nPRESS ENTER TO EXIT SUMMARY...")  # to be removed - helps with testing
