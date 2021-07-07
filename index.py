#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import functions from additional files
from read_file import import_file
from calculate_file import calculate_arrhenius, calculate_dae
from write_file import save_arrhenius, save_dae
from plot_file import make_plot

# START XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Welcome message
print('\nWelcome to program!')

# Import file
data, delimeter, coma, data_names = import_file()

# Calculator Arrhenius
data_arrhenius, r2_table, p_list, p_step = calculate_arrhenius(data, data_names)

# Save Arrhenius data
saved_files = save_arrhenius(data_arrhenius, data_names, delimeter, coma, r2_table)

#Calculator DAE
data_dae = calculate_dae(data, data_names)

# Save DAE data
saved_files = save_dae(data_dae, data_names, delimeter, coma, saved_files)

# Plot
make_plot(data, data_names, data_dae, r2_table)

input('\n\nPRESS ENTER TO EXIT...') # to be removed - helps in testing
