#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pandas as pd
import pathlib

# FUNCTIONS
# Import file
def save_file(data, data_names, delimeter :str, coma :str, r2p):
    x = -1
    saved_files = []
    
    pathlib.Path('Results/').mkdir(parents=True, exist_ok=True)

    r2p.to_csv('Results/r2p.txt', index=False, sep =delimeter, decimal =coma)
    saved_files.append('Results/r2p.txt')

    for i in data_names:
        x += 1
        data_temp = data[x]
        data_path = 'Results/' + i + '.txt'     
        data_temp.to_csv(data_path, index=False, sep =delimeter, decimal =coma)
    
        saved_files.append(data_path)

    print('\nFiles saved:')
    for count, item in enumerate(saved_files, 0):
        print(count, item)
    return
