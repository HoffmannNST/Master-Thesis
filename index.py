#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import functions from additional files
from read_file import import_file
from calculate_file import calculate_arrhenius, calculate_dae
from write_file import save_file
from plot_file import make_plot

# START XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Welcome message
print('\nWelcome to program!')

# Import file
data, delimeter, coma, data_names = import_file()

# Calculator Arrhenius
data, r2p = calculate_arrhenius(data, data_names)

#Calculator DAE
calculate_dae(data, data_names)

# Save file
save_file(data, data_names, delimeter, coma, r2p)

# Plot
make_plot(r2p, data_names, data)

input('\n\nPRESS ENTER...')
