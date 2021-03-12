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
except FileNotFoundError:
    print('\nSpecified file does not exist or file path is incorrect!\n')
