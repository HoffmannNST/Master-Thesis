#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pandas as pd
# import numpy as np
# import matplotlib as mtp

# Import functions from additional files
from read_file import import_file
from calculate_file import calculator

# Predefined settings
calc_set = 'index'          # working with columns indexes or names
data_loaded = False         # no data is loaded at the beggining of program
step_back = ['x','X']       # keywords to break current loop and go back to previous menu
close_program = ['x','X']   # keywords to exit program from the MENU

            
# START XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Welcome message
print('\nWelcome to program!')

# Continous loop of program
while True:

    # MENU
    menu = input('\nMENU:\n1 - Import file to program\n2 - Calculator\n3 - Option unavailable yet\nX - Close program\n\nSelect one of the above by entering suitable symbol: ')

    if menu in close_program:
        break

    elif menu == '1':   # Import file
        data_loaded, data = import_file()

    elif menu == '2':   # Calculator
        calc_set, data = calculator(data_loaded, calc_set, data)

    # elif menu == '3': # Option 3
        # option3()

    else:
        input('\nIncorrect option!\nPress ENTER to continue...')
