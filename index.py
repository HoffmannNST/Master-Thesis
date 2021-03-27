#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import functions from additional files
from read_file import import_file
from calculate_file import calculate
from write_file import save_file

# START XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Welcome message
print('\nWelcome to program!')

# Import file
data, loaded_files, delimeter, coma = import_file()

# Calculator
data = calculate(data, loaded_files)

# Save file
save_file(data, loaded_files, delimeter, coma)

input('\n\nPRESS ENTER...')
