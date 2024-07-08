'''
Calculates the "secretary problem" outcome based bon given values
Single core calculation
'''
import os
import sys
import time

import math
import numpy as np
import pandas as pd

# Based on example:
# https://imrankhan17.github.io/pages/Solving%20the%20secretary%20problem%20with%20Python.html

# Inputs
# The higher the value the more presice the values (100000 is sufficient)
CYCLES = 800
# Potential dating partners
POPULATION = 10
# Min value (0 would give nicer averages but no one would date a literal 0)
MIN_VAL = 1
# Max value, assuming there is no IMPROVEMENT in partners with time
MAX_VAL = 100

# IMPROVEMENT variable by
IMPROVEMENT = 1
# Limit on maximum highest value
MAX_VAL_LIMIT = 200
# In case it gets only worse
MIN_VAL_LIMIT = 0

# Steps taken from zero to max population
# If you don't want to do STEPs make STEPs same or bigger than population
STEP = 10

result_folder = os.getcwd() + '\\Results'

if not os.path.exists(result_folder):
    os.makedirs(result_folder)

os.chdir(result_folder)

# Create file name for resulting table
test_name = f'Pop {POPULATION} Cy {CYCLES} Min {MIN_VAL} Max {MAX_VAL} \
Imp {IMPROVEMENT} Upper {MAX_VAL_LIMIT} Bottom {MIN_VAL_LIMIT}.csv'

# Check if filename exists, then don"t repeat it
# https://stackoverflow.com/a/179608/5531122
if os.path.isfile(test_name):
    sys.exit('Already Genarated')

# Variables
filler = np.empty(1)
increm = np.empty(1)

# Baseline result holders
baseline_total = np.zeros(POPULATION)
baseline_best = np.zeros(POPULATION)

# Results
total = np.zeros(POPULATION)
the_best = np.zeros(POPULATION)
top_95 = np.zeros(POPULATION)
top_90 = np.zeros(POPULATION)
top_80 = np.zeros(POPULATION)

# Saving
header = np.arange(1,POPULATION+1)

# Checking inputs
if IMPROVEMENT != 1:
    increm = np.linspace(1,IMPROVEMENT,endpoint=True,num=POPULATION)
    np.around(increm,decimals=round(math.log(POPULATION,10)+2),out=increm)

MAX_VAL_LIMIT = max(MAX_VAL_LIMIT, MAX_VAL*IMPROVEMENT)



# Generating single array
# Start time
time_start = time.time()

# Single array
for k in range(CYCLES):
    # Get the desired population regardless based on given min and max
    if MAX_VAL - MIN_VAL == POPULATION:
        filler = np.arange(MIN_VAL,MAX_VAL+1)
    elif MAX_VAL - MIN_VAL > POPULATION:
        filler  = np.arange(MIN_VAL,POPULATION+MIN_VAL)
    else:
        filler = np.arange(MIN_VAL,MAX_VAL+1)
        extra = np.random.randint(MIN_VAL,high=MAX_VAL,
            size=POPULATION-filler.shape[0])
        filler = np.concatenate([filler,extra])

    np.random.shuffle(filler)

    # Recalculate for improvement
    if IMPROVEMENT != 1:
        filler = filler*increm
        if MAX_VAL * IMPROVEMENT > MAX_VAL_LIMIT:
            filler[filler > MAX_VAL_LIMIT] = MAX_VAL_LIMIT
        if MAX_VAL * IMPROVEMENT < MIN_VAL_LIMIT:
            filler[filler < MIN_VAL_LIMIT] = MIN_VAL_LIMIT
        np.around(filler,decimals=0,out=filler)
        # print(filler)
        filler = filler.astype(int)
        # print(filler)

    # Values for Top 95%, 90%, 80% of partners
    value_at_95 = math.ceil((np.amax(filler)-np.amin(filler))*0.95)
    value_at_90 = math.ceil((np.amax(filler)-np.amin(filler))*0.90)
    value_at_80 = math.ceil((np.amax(filler)-np.amin(filler))*0.80)

    # Baseline
    np.add(baseline_total,filler, out=baseline_total)
    baseline_best[np.argmax(filler)] += 1

    # Comparing to the best so far

    for i in range(POPULATION-1):
        #  If max value was already seen skip the comparison
        if np.amax(filler[:i+1]) >= np.amax(filler):
            total[i] += filler[-1]

        else:
            x = np.argmax(filler[i:] > np.amax(filler[:i+1])) + i
            total[i] += filler[x]

            # Filling target values
            if filler[x] == np.amax(filler):
                the_best[i] += 1
            elif filler[x] >= value_at_95:
                top_95[i] += 1
            elif filler[x] >= value_at_90:
                top_90[i] += 1
            elif filler[x] >= value_at_80:
                top_80[i] += 1

    # Evaluating last position
    total[-1] += filler[-1]
    if filler[-1] == np.amax(filler):
        the_best[-1] += 1


    # Prints progress and time left
    if k % (CYCLES/100)  == 0 and k/CYCLES*100 >= 1:
        progress = int(k/CYCLES*100)

        #Calculate time left
        time_current = time.time()
        diff = time_current - time_start
        time_left = diff/progress * (100-progress)

        # Print time untill Finished
        # https://stackoverflow.com/a/27780763/55311220
        hours, rem = divmod(time_left, 3600)
        minutes, seconds = divmod(rem, 60)
        print(f'{progress:>2d} %  -  Remaining Time: '
            f'{int(hours):0>2}:{int(minutes):0>2}:{seconds:01.1f}')

np.set_printoptions(precision=4, suppress = True)


# Saving Data
finished = np.column_stack((
    baseline_total/CYCLES/POPULATION,
    baseline_best/CYCLES,
    total/CYCLES/POPULATION,
    the_best/CYCLES,
    top_95/CYCLES,
    top_90/CYCLES,
    top_80/CYCLES))

# https://stackoverflow.com/a/11146434/5531122

names  = ['baseline_total', 'baseline_best', 'total',
    'the_best', 'top_95', 'top_90', 'top_80']

df = pd.DataFrame(finished, columns=names)
# https://stackoverflow.com/a/20168394/5531122
df.index = np.arange(1, len(df)+1)
df.to_csv(test_name, index=True, header=True, sep=' ')

if __name__== "__main__":
