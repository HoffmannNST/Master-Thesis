#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import functions from additional files
from read_file import import_file, get_column_names, read_config
from calculate_file import (
    calculate_arrhenius,
    calculate_dae,
    p_steps_f,
    theoretical_arrhenius,
)
from write_file import (
    save_arrhenius,
    save_summary_arrhenius,
    save_dae,
    save_summary_dae,
)
from plot_file import (
    make_plot_call,
    simulate_r_t,
    plot_arrhenius,
    plot_r_t,
    plot_r2_p,
    plot_dae,
    plot_theoretical_arrhenius,
)

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
    theoretical_p_list,
    simulate,
    simulate_t_min,
    simulate_t_max,
    simulate_t_step,
    simulate_r0_param,
    simulate_t0_param,
    simulate_p_param,
) = read_config()

# Import file
data, delimeter, decimal_separator, loaded_files = import_file(
    read_directory,
    data_file_format,
    delimeter,
    decimal_separator,
)

# Select columns in dataframe
column_t_name, column_r_name = get_column_names(
    data,
    column_t_index,
    column_r_index,
)

# Choosing fitting range of p parameter
p_list = p_steps_f(p_step, p_range_min, p_range_max)

# Calculate Arrhenius method in set range
data_arrhenius, r2_table, list_arr_params = calculate_arrhenius(
    data,
    loaded_files,
    p_list,
    p_step,
    column_t_name,
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
)

# Save summary Arrhenius data
saved_files = save_summary_arrhenius(
    loaded_files,
    save_directory,
    list_arr_params,
)

# Calculate Arrhenius method with theoretical p values
arr_theoretical_params_list = theoretical_arrhenius(
    data_arrhenius,
    loaded_files,
    column_t_name,
    column_r_name,
    theoretical_p_list,
)

# Calculate DAE method
(
    data_dae,
    list_p_optimal,
    list_dae_r2_score,
    list_dae_regress,
    list_dae_params_allometric,
    list_dae_params_log,
) = calculate_dae(data, loaded_files, column_t_name, column_r_name)

# Save DAE data
saved_files = save_dae(
    data_dae,
    loaded_files,
    delimeter,
    decimal_separator,
    saved_files,
    save_directory,
)

# Save summary DAE data
saved_files = save_summary_dae(
    loaded_files,
    list_p_optimal,
    list_dae_r2_score,
    saved_files,
    list_dae_regress,
    list_dae_params_allometric,
    list_dae_params_log,
    save_directory,
)

# Plot single plots
plot_file_count = make_plot_call(
    data,
    loaded_files,
    data_dae,
    data_arrhenius,
    r2_table,
    list_p_optimal,
    column_t_name,
    column_r_name,
    save_directory,
    list_dae_r2_score,
    list_dae_regress,
    list_arr_params,
)

# Plot arrhenius plots calculated with theoretical p values
plot_file_count = plot_theoretical_arrhenius(
    loaded_files,
    data_dae,
    column_t_name,
    theoretical_p_list,
    arr_theoretical_params_list,
    save_directory,
    plot_file_count,
)

# Plot multiple arrhenius plots
plot_file_count = plot_arrhenius(
    data_arrhenius,
    loaded_files,
    list_arr_params,
    plot_file_count,
    save_directory,
)

# Plot multiple R(T) plots
plot_file_count = plot_r_t(
    loaded_files, column_t_name, column_r_name, data, save_directory, plot_file_count
)

# Plot multiple R^2(p) plots
plot_file_count = plot_r2_p(r2_table, loaded_files, save_directory, plot_file_count)

# Plot multiple DAE(T) plots
plot_file_count = plot_dae(
    loaded_files, data_dae, column_t_name, save_directory, plot_file_count
)

# Simulate R(T) data using user's parameters
if simulate:
    simulate_r_t(
        simulate_t_min,
        simulate_t_max,
        simulate_t_step,
        simulate_r0_param,
        simulate_t0_param,
        simulate_p_param,
        save_directory,
        plot_file_count,
    )

input("\nPRESS ENTER TO EXIT SUMMARY...")  # to be removed - helps with testing
