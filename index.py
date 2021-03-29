#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import functions from additional files
from read_file import import_file
from calculate_file import calculate
from write_file import save_file
from plot_file import do_plot

# START XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Welcome message
print('\nWelcome to program!')

# Import file
data, delimeter, coma, data_names = import_file()

# Calculator
data, r2p = calculate(data, data_names)

# Save file
save_file(data, data_names, delimeter, coma)

# Plot
do_plot(r2p, data_names)

input('\n\nPRESS ENTER...')
