# Program for automation of analysis and interpretation of resistance vs temperature data in terms of determining the model of electrical conductivity.

This program is made by Nicolas Hoffmann as the part of Master thesis at Poznań University of Technology.

## Installation
The program has been compiled to executable application. Therfore there is no need for installation of any packages. The program is available at [this link](https://drive.google.com/file/d/19gqg7t_HqkwY2mtjpt0WuMQV9NZYKfla/view?usp=sharing).

In order to run the program user needs to download the .zip file from the link above and unpack it in desired disk location. From here user is able to configure program's settings and run the program.

## Usage
In order to run program properly user needs to configure program's settings. All setting can be found in configuration file named "config.yml". The file is located in "./dist/index/" directory of unpacked program. 

In this configuration file user needs to specify path to folder containing data. The data file needs to have two columns, one containing temperature data and other containing resistance data. Those two columns have to be specified in configuration file, as the data file can contain more than 2 columns. The columns in data file need to have column labels in first row of data. In configuration file user needs to specify format of data files, column separator and decimal separator. User also needs to specify path to results folder where data will be saved. Program allows calculations for specified range of "p" parameter and for specified theoretical values of "p" parameter, which need to be set in configuration file. If set in configuration file program will also simulate R(T) curve with set parameters.

With all variables in "config.yml" set correctly user may run the program by launching "index.exe" file that is located in "./dist/index/" directory of the unpacked program. The program will proceed to calculations and ploting of data. All calculation results will be shown in summary in console. More data and plots can be found in specified results path.

## Results

Results data are sorted into three folders.

First named "Arrhenius" contains results data for every input data file containg all data needed for Arrhenius curves calculations. It also contains "r2p_arr" file, in which data is stored, allowing for the plotting of the relationship of the linear regression fit coefficient as a function of the "p" parameter for all measurement series. The last file in this folder is the "Arrhenius_summary" file, in which the "p", "R0vrh" and "T0vrh" parameters are stored for each measurement series. 

In the second folder called "DAE" there are files for each measurement series containing temperature and resistance data as well as all the data needed to calculate and determine the differential activation energy versus temperature, as well as the logarithm of the differential activation energy versus the logarithm of temperature. The "DAE_summary" file located in this folder contains a summary of all measurement series in which the values of the coefficients determined from linear and nonlinear regression as well as the values of p and T0vrh parameters determined from the dependence of DAE on T and log (DAE) on log (T) are stored.

The last folder named "Plots" contains all the graphs created by the program sorted in folders corresponding to the names of the measurement series. There are four plots created as summary with all the measurement series. which are:
- resistance versus temperature,
- linear regression fit coefficient versus "p" parameter,
- differential activation energy versus temperature,
- Arrhenius curves.

In addition there are created separate folders for all the measurement series whoch contains seven plots for each series. Those plots are:
- resistance versus temperature,
- resistance versus temperature with best Arrhenius fit,
- linear regression fit coefficient versus "p" parameter,
- differential activation energy versus temperature,
- differential activation energy versus temperature with best Arrhenius fit,
- differential activation energy versus temperature with Arrhenius fits for all theoretical "p" parameters,
- logarithm of the differential activation energy versus the logarithm of temperature.

## Theory

Program follows calculations for Variable Range Hopping (VRH) model of electrical conductivity using Arrhenius curves method as well as differential activation energy method. Using equations for VRH equations for calculations also allows analysis of resulting data for Nearest Neighbour Hopping (NNH) and Band Conductivity (BC) models of electrical conductivity. Calculations contain linear and nonlinear regression, discrete deriviative and logarithm operations. More informations on models of electrical conductivity and calculations may be found in relevant publications.

## Licence and contact information

This program is made by Nicolas Hoffmann as the part of Master thesis at Poznań University of Technology. I am not offering any license for this project.

You can contact me via email: nicolashoffmann97@gmail.com
