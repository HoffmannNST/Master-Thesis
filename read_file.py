#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pandas as pd

# Predefined settings
data_loaded = False         # no data is loaded at the beggining of program
step_back = ['x','X']       # keywords to break current loop and go back to previous menu

# FUNCTIONS
# Read file
def get_file(path: str, coma: str):
    imported_file = pd.read_csv(path, sep ='\t', decimal =coma, header =0)
    return imported_file

# Import file
def import_file():
    global data
    while True:
        #path = input('\nSpecify file path:\n')
        path = 'test.txt'
        if path in step_back:       # Back to MENU
            break

        #decimal = input('\nSpecify decimal separator in the file:\n')     # '.' or ','
        decimal = ','
        if decimal in step_back:    # Back to MENU
            break

        try:
            data = get_file(path, decimal)
            print('\n',data,'\n')
            return True, data		# True for data_loaded

        except FileNotFoundError:
            back = input('\nSpecified file does not exist or file path is incorrect!\nType X to exit to menu   or   press ENTER to continue...')
            if back in step_back:   # Back to MENU
                break
