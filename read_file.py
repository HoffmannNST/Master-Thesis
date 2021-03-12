#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pandas as pd
#import numpy as np
#import matplotlib as mtp 


# Read file
def read_file(x,y):
    test_file = pd.read_csv(x, sep='\t', decimal=y, index_col = 0)
    return test_file

# Welcome message
print('\nWelcome to program!')

# Continous loop of program
while True:

    # MENU
    menu = str(input('\nMENU:\n1 - Import file to program\n2 - Option unavailable yet\n3 - Option unavailable yet\n4 - Close program\n\nSelect one of the above by entering suitable number: '))

    if menu == '4':
        break
    elif menu == '1':
        while True:
            # Get file path
            path = str(input('\nSpecify file path:\n'))
            #path = 'test.txt'

            # Specify decimal separator in the file (, or .)
            decimal = str(input('\nSpecify decimal separator in the file:\n'))
            #decimal = ','

            # Get and print data
            try:
                data = read_file(path, decimal)
                print('\n',data,'\n')
                break
            except FileNotFoundError:
                back = str(input('\nSpecified file does not exist or file path is incorrect!\nType X to exit to menu   or   press ENTER to continue...'))
                if back == 'x' or back == 'X':
                    break
    else:
        input('\nIncorrect option!\nPress ENTER to continue...')
