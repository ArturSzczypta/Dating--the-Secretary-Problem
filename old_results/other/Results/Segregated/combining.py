import multiprocessing as mp
import numpy as np

import math
import time
import os
import sys

import pandas as pd
import glob


cycles = 100000
# Potential dating partners
population = 1000
# Min value (0 would give nicer averages but no one would date a literal 0)
min_val = 1
# Max value (if there'san improvement it will go up with time)
max_val = 1000

# How much you'll improve until the end (1.0 - no improvement, 1.5 - 50% improvement)
improvement = 1.0
# In case you are or become soo attractive that you can hit the limit
upperCeeling = 2000
# In case it gets only worse
bedrock = 0


#Based on
#https://www.freecodecamp.org/news/how-to-combine-multiple-csv-files-with-8-lines-of-code-265183e0854/

result_folder = os.getcwd() + '\\c'
os.chdir(result_folder)

extension = 'csv'

test_name = 'Combined Pop ' + str(population) + ' Cy ' \
			+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
			+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) \
			+ ' Bottom ' + str(bedrock)+ '.csv'


#finished  = np.zeros((7,population))

#merging = np.zeros((7,population))

# No Need for shared arrays
#https://stackoverflow.com/a/44703026/5531122
#np.set_printoptions(precision=7, suppress = True)

#finished = merging

# use glob to ,atch pattern 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#print(all_filenames)
#Combine all files in the list and export as csv
#df = pd.DataFrame(pd.concat([pd.read_csv(f) for f in all_filenames]))
df  = pd.concat([pd.read_csv(f,delim_whitespace=True).reset_index() for f in all_filenames])

#df = pd.read_csv('combined_csv.csv',delim_whitespace=True)
print(df)


print([*df])
print('--')
print(df.head())
print('---')
print(df.columns)
print('-----')

df.rename({df.columns[0]:'position'}, axis='columns', inplace=True)


#https://stackoverflow.com/a/39919681/5531122
averaged = df.groupby('position').mean().reset_index()
print(averaged)


averaged.to_csv(test_name, index=False, header=True, sep=' ')

