#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# m Import packages
import pandas as pd
# import numpy as np
# import matplotlib as mtp

# Predefined settings
calc_set = 'num'            # num or nam - working with columns numbers or names
data_loaded = False         # no data is loaded at the beggining of program
step_back = ['x','X']       # keywords to break current loop and go back to previous menu
close_program = ['x','X']   # keywords to exit program from the MENU

# FUNCTIONS
# Read file
def read_file(path: str, coma: str):
    imported_file = pd.read_csv(path, sep ='\t', decimal =coma, header =0)
    return imported_file

# Import file
def import_file():
    global data
    global data_loaded
    while True:
        #path = str(input('\nSpecify file path:\n'))
        path = 'test.txt'
        if path in step_back:       # Back to MENU
            break

        #decimal = str(input('\nSpecify decimal separator in the file:\n'))     # '.' or ','
        decimal = ','
        if decimal in step_back:    # Back to MENU
            break

        try:
            data = read_file(path, decimal)
            print('\n',data,'\n')
            data_loaded = True
            break
        except FileNotFoundError:
            back = input('\nSpecified file does not exist or file path is incorrect!\nType X to exit to menu   or   press ENTER to continue...')
            if back in step_back:   # Back to MENU
                break

# Choose column to edit in the Calculator
def choose_column(setting: str):
    if setting == 'num':
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
def calc_operate(operation: str, column: int or str, number: float):
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
    global calc_set
    while True:
        calc_set = input('Do you want to work with column numbers or names (enter num or nam): ')
        if calc_set in step_back:   # Back to MENU
            calc_set = 'num'
            break
        elif calc_set == 'num' or calc_set == 'nam':
            break

# Calulate
def calculator():
    global calc_set
    print('funkcja start')
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
                        data.iloc[:,[edit_column]] = calc_operate(calc_operation, edit_column, calc_number)
                        print('\nDATA AFTER\n', data.iloc[[0,1,2,3],[edit_column]])     #line for testing, to be deleted later
                    elif calc_set == 'nam':
                        print('\nDATA BEFORE\n', data.loc[[0,1,2,3],[edit_column]])     #line for testing, to be deleted later
                        data.loc[:,[edit_column]] = calc_operate(calc_operation, edit_column, calc_number)
                        print('\nDATA AFTER\n', data.loc[[0,1,2,3],[edit_column]])      #line for testing, to be deleted later
                except IndexError:
                    print('Column index out of range!\n')
                except KeyError:
                    print('Column label not found!\n')

        elif menu_calc == '2':      # Create new column
            pass

        elif menu_calc == '3':      # Settings
            calculator_settings()
            
# START XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Welcome message
print('\nWelcome to program!')

# Continous loop of program
while True:

    # MENU
    menu = input('\nMENU:\n1 - Import file to program\n2 - Calculator\n3 - Option unavailable yet\nX - Close program\n\nSelect one of the above by entering suitable symbol: ')

    if menu in close_program:
        break

    # OPTION 1 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    elif menu == '1':   # Import file
        import_file()

    # OPTION 2 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    elif menu == '2':   # Calculator
        calculator()

    # OPTION 3 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    # elif menu == '3':
        # option3()

    else:
        input('\nIncorrect option!\nPress ENTER to continue...')
