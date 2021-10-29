#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import functions from additional files
from read_file import import_file, get_column_names, read_config
from calculate_file import calculate_arrhenius, calculate_dae, p_steps_f
from write_file import save_arrhenius, save_dae
from plot_file import make_plot_call

# START XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Welcome message
print("\nWelcome to program!")

# Read user's program configuration
(
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
) = read_config()

# Import file
data, delimeter, decimal_separator, loaded_files = import_file(
    read_directory,
    data_file_format,
    delimeter,
    decimal_separator,
)

# Select columns in dataframe
column_T_name, column_r_name = get_column_names(
    data,
    column_t_index,
    column_r_index,
)

# Choosing fitting range of p parameter
p_list = p_steps_f(p_step, p_range_min, p_range_max)

# Calculate Arrhenius method
data_arrhenius, r2_table, list_arr_params = calculate_arrhenius(
    data,
    loaded_files,
    p_list,
    p_step,
    column_T_name,
    column_r_name,
    p_range_min,
    p_range_max,
)

# Save Arrhenius data
saved_files = save_arrhenius(
    data_arrhenius,
    loaded_files,
    delimeter,
    decimal_separator,
    r2_table,
    save_directory,
    list_arr_params,
)

# Calculate DAE method
(
    data_dae,
    list_p_optimal,
    list_dae_r2_score,
    list_dae_regress,
    list_dae_params,
) = calculate_dae(data, loaded_files, column_T_name, column_r_name)

# Save DAE data
saved_files = save_dae(
    data_dae,
    loaded_files,
    delimeter,
    decimal_separator,
    saved_files,
    list_p_optimal,
    list_dae_r2_score,
    list_dae_regress,
    list_dae_params,
    save_directory,
)

# Plot
make_plot_call(
    data,
    loaded_files,
    data_dae,
    r2_table,
    list_p_optimal,
    column_T_name,
    column_r_name,
    save_directory,
    list_dae_r2_score,
)

input("\nPRESS ENTER TO EXIT SUMMARY...")  # to be removed - helps with testing
