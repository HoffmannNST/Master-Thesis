#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pandas as pd
import pathlib
# import matplotlib as mtp

# Import functions from additional files
from read_file import import_file
#from calculate_file import calculator

# Predefined settings
calc_set = 'index'          # working with columns indexes or names
data_loaded = False         # no data is loaded at the beggining of program
data = []

            
# START XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Welcome message
print('\nWelcome to program!')

# Import file
data = import_file()

# Calculator
#data = calculator(data)

# Option 3
#option3()
