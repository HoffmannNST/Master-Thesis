#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pandas as pd
#import numpy as np
#import matplotlib as mtp 

#FUNCTIONS
# Read file
def read_file(x,y):         # x - str(path); y - str(',' or '.');
    imported_file = pd.read_csv(x, sep ='\t', decimal=y, header=0)
    return imported_file

# Choose column to edit in the Calculator
def choose_column(x):       # x - str(calc_set);
    if x == 'num':
        chosen_column = int(input('\nChoose a column to edit: '))
    elif x =='nam':
        chosen_column = (input('\nChoose a column to edit: '))
    return chosen_column

# Operate on data in Calculator
def calc_operate(x,y,z):       # x - str(calc_operation); y - str or int(edit_column); z - float(calc_number);
    if x == '+':
        data.iloc[:,[y]] = data.iloc[:,[y]] + z
    elif x == '-':
        data.iloc[:,[y]] = data.iloc[:,[y]] - z
    elif x == '*':
        data.iloc[:,[y]] = data.iloc[:,[y]] * z
    elif x == '/':
        data.iloc[:,[y]] = data.iloc[:,[y]] / z
    elif x == '**':
        data.iloc[:,[y]] = data.iloc[:,[y]] ** z
    return data.iloc[:,[y]]

# Predefined settings
calc_set = 'num'            # num or nam - working with columns numbers or names
data_loaded = False         # no data is loaded at the beggining of program
step_back = {'x','X'}       # keywords to break current loop and go back to previous menu
close_program ={'x','X'}    # keywords to exit program from the MENU

#START XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
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
        while True:
            # Get file path
            path = str(input('\nSpecify file path:\n'))
            #path = 'test.txt'
            if path in step_back:       # Back to MENU
                break

            # Specify decimal separator in the file (, or .)
            decimal = str(input('\nSpecify decimal separator in the file:\n'))
            #decimal = ','
            if decimal in step_back:    # Back to MENU
                break

            # Get and print data
            try:
                data = read_file(path, decimal)
                print('\n',data,'\n')
                data_loaded = True
                break
            except FileNotFoundError:
                back = input('\nSpecified file does not exist or file path is incorrect!\nType X to exit to menu   or   press ENTER to continue...')
                if back in step_back:   # Back to MENU
                    break

    # OPTION 2 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    elif menu == '2':   # Calculator
        while True:
            # Test if there is any file imported to program
            if data_loaded == False:    
                input('\nNo data has been loaded yet! Please imoprt a file.\nPress ENTER to continue...')
                break
            
            # Menu for calculator options
            calculator = input('\nCALCULATOR:\n1 - Edit a column\n2 - Create new column\n3 - Settings\nX - Exit to menu\n\nSelect one of the above by entering suitable number: ')
            
            if calculator in step_back:
                break

            elif calculator == '1':     # Edit column
                while True:
                    edit_column = choose_column(calc_set) # Select column to edit
                    if edit_column in step_back: # back to the Calculator menu
                        break

                    calc_operation = input('Choose operation (+, -, *, /, **): ')
                    calc_number = float(input('Choose a number to make operation with (i.e. -2.143): '))

                    print('\nDATA BEFORE\n', data.iloc[[0,1,2,3],[edit_column]])    #line for testing, to be deleted later
                    data.iloc[:,[edit_column]] = calc_operate(calc_operation, edit_column, calc_number)
                    print('\nDATA AFTER\n', data.iloc[[0,1,2,3],[edit_column]])     #line for testing, to be deleted later

            elif calculator == '2':     # Create new column
                pass

            elif calculator == '3':     # Settings
                calc_set = input('Do you want to work with column numbers or names (enter num or nam): ')

            input("\nIT'S OK! PRESS ENTER") #line for testing, to be deleted later

    # OPTION 3 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    #elif menu == '3':
        #while True:
        #break

    else:
        input('\nIncorrect option!\nPress ENTER to continue...')
