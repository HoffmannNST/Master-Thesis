#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pandas as pd

# Import functions from additional files
from read_file import import_file

# Predefined settings
calc_set = 'num'            # num or nam - working with columns numbers or names
data_loaded = False         # no data is loaded at the beggining of program
step_back = ['x','X']       # keywords to break current loop and go back to previous menu
close_program = ['x','X']   # keywords to exit program from the MENU
data = pd.Series()

# FUNCTIONS
# Choose column to edit in the Calculator
def choose_column(calc_set: str):
    if calc_set == 'num':
        while True:
            try:
                chosen_column = input('\nChoose a column to edit: ')
                if chosen_column in step_back:  # back to the Calculator menu
                    break
                chosen_column = int(chosen_column)
                break
            except ValueError:
                print('Faulty input!!')
    else:
        chosen_column = (input('\nChoose a column to edit: '))
    return chosen_column

# Operate on data in Calculator
def calc_operate(calc_set: str, data, operation: str, column: int or str, number: float):
    if calc_set == 'num':
        result = data.iloc[:,[column]]
    else:
        result = data.loc[:,[column]]
    
    if operation == '+':
        result += number
    elif operation == '-':
        result -= number
    elif operation == '*':
        result *= number
    elif operation == '/':
        result /= number
    elif operation == '**':
        result **= number
    return result

# Calculator settings
def calculator_settings():
    while True:
        calc_set = input('Do you want to work with column numbers or names (enter num or nam): ')
        if calc_set in step_back:   # Back to MENU
            break
        elif calc_set == 'num':
            return 'num'
        elif calc_set == 'nam':
            return 'nam'

# Calulate
def calculator(data_loaded, calc_set, data):
    while True:
        # Test if there is any file imported to program
        if data_loaded == False:    
            input('\nNo data has been loaded yet! Please imoprt a file.\nPress ENTER to continue...')
            break
            
        # Menu for calculator options
        menu_calc = input('\nCALCULATOR:\n1 - Edit a column\n2 - Create new column\n3 - Settings\nX - Exit to menu\n\nSelect one of the above by entering suitable number: ')
            
        if menu_calc in step_back:  # Back to MENU
            break

        elif menu_calc == '1':      # Edit column
            while True:
                edit_column = choose_column(calc_set)   # Select column to edit
                if edit_column in step_back:            # back to the Calculator menu
                    break

                calc_operation = input('Choose operation (+, -, *, /, **): ')
                if calc_operation in step_back:
                            break

                calc_number = float(input('Choose a number to make operation with (i.e. -2.143): '))
                if calc_operation == '/' and calc_number == 0:
                    while calc_number == 0:
                        print('Division by 0!!!')
                        calc_number = float(input('Choose a number to make operation with (i.e. -2.143): '))
                        if calc_number in step_back:
                            break
                if calc_number in step_back:
                            break
                try:
                    if calc_set == 'num':
                        print('\nDATA BEFORE\n', data.iloc[[0,1,2,3],[edit_column]])    #line for testing, to be deleted later
                        data.iloc[:,[edit_column]] = calc_operate(calc_set, data, calc_operation, edit_column, calc_number)
                        print('\nDATA AFTER\n', data.iloc[[0,1,2,3],[edit_column]])     #line for testing, to be deleted later
                    elif calc_set == 'nam':
                        print('\nDATA BEFORE\n', data.loc[[0,1,2,3],[edit_column]])     #line for testing, to be deleted later
                        data.loc[:,[edit_column]] = calc_operate(calc_set, data, calc_operation, edit_column, calc_number)
                        print('\nDATA AFTER\n', data.loc[[0,1,2,3],[edit_column]])      #line for testing, to be deleted later
                except IndexError:
                    print('Column index out of range!\n')
                except KeyError:
                    print('Column label not found!\n')

        elif menu_calc == '2':      # Create new column
            pass

        elif menu_calc == '3':      # Settings
            calc_set = calculator_settings()

    return calc_set, data
        