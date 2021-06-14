#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import functions from additional files
from read_file import import_file
from calculate_file import calculate_arrhenius, calculate_dae
from write_file import save_file
from plot_file import make_plot

# START XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
print('\nWelcome to program!')

# Import file
data, delimeter, coma, data_names = import_file()

# Calculator Arrhenius
data_arr, r2_table, p_list, p_step = calculate_arrhenius(data, data_names)

#Calculator DAE
data_dae = calculate_dae(data, data_names, p_list, p_step)

# Save file
save_file(data_arr, data_dae, data_names, delimeter, coma, r2_table)

# Plot
make_plot(r2_table, data_names, data, data_dae)

input('\n\nPRESS ENTER TO EXIT...')
