#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import pandas as pd
import pathlib

# FUNCTIONS
# Import file
def save_file(data, loaded_files, delimeter :str, coma :str):
    x = -1
    saved_files = []
    
    pathlib.Path('Results/').mkdir(parents=True, exist_ok=True)

    for i in loaded_files:
        x += 1
        data_temp = data[x]
        data_path = 'Results/'
        
        if 'chlodzenie' in i:
            data_path += 'chlodzenie'
            if '2400' in i:
                data_path += '2400.txt'     # .txt can be changed to .csv or other format
                data_temp.to_csv(data_path, index=False, sep =delimeter, decimal =coma)
            elif '2000' in i:
                data_path += '2000.txt'
                data_temp.to_csv(data_path, index=False, sep =delimeter, decimal =coma)
        elif 'grzanie' in i:
            data_path += 'grzanie'
            if '2400' in i:
                data_path += '2400.txt'
                data_temp.to_csv(data_path, index=False, sep =delimeter, decimal =coma)
            elif '2000' in i:
                data_path += '2000.txt'
                data_temp.to_csv(data_path, index=False, sep =delimeter, decimal =coma)
        
        saved_files.append(data_path)

    print('\nFiles saved:')
    for count, item in enumerate(saved_files, 0):
        print(count, item)
    return
