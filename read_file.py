#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pandas as pd
#import numpy as np
#import matplotlib as mtp 

# Reading File
def read_file(x):
    test_file = pd.read_csv(x, sep='\t', decimal=',') # "index_col = 0" deleting 1st column with iteration
    return test_file

path = 'test.txt'
data = read_file(path)

print(data)