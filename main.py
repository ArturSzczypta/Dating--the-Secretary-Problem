'''Generates a csv files with the results of "the secretary problem"
I decided to leave some hyperlinks to stackoverflow'''

import multiprocessing as mp
import numpy as np
import logging
from pathlib import Path
import logging_files.logging_function as l_f

import math
import time
import os
import sys

import pandas as pd

current_file_name = Path(__file__).stem
log_file_name = f'{current_file_name}_log.log'

BASE_DIR = Path(__file__).parent
LOGGING_FILE = BASE_DIR / 'logging_files' / log_file_name
LOGGING_JSON = BASE_DIR / 'logging_files' / 'logging_config.json'

l_f.configure_logging(LOGGING_JSON, LOGGING_FILE)

# Potential dating partners
POPULATION = 100
# How many times to run the simulation
CYCLES = 10000
# Min value (0 would give nicer averages but no one would date a literal 0)
MIN_VAL = 1
# Max value (if there's an improvement it will go up with time)
MAX_VAL = 100
# How much you'll improve until the end (1.0 - no improvement, 1.5 - 50% impr.)
IMPROVEMENT = 1
# In case it gets only worse
MIN_VAL_LIMIT = 0
# In case you are or become soo attractive that you can hit the limit
MAX_VAL_LIMIT = 109

if MAX_VAL_LIMIT <= MAX_VAL:
    MAX_VAL_LIMIT = MAX_VAL

MULTIPROCESS = True
PROCESSORS = mp.cpu_count()

# Estimate after 0.001%, 0.01%, 0.1%, 1%, 10%
samples = [CYCLES/100000, CYCLES/10000, CYCLES/1000, CYCLES/100,CYCLES/10]

if MULTIPROCESS:
    logging.info(f'Number of cores: {PROCESSORS}')
    samples *= PROCESSORS

samples = [math.floor(sample) for sample in samples]
samples = [sample for sample in samples if sample > 10]
logging.debug(f'Samles to use for time estimate: {samples}')

result_folder = Path.cwd() / 'Results'
if not result_folder.exists():
    result_folder.mkdir(parents=True)
os.chdir(result_folder)

basic_name = f'''pop {POPULATION} cy {CYCLES} imp {IMPROVEMENT} min {MIN_VAL} \
    max {MAX_VAL} bottom {MIN_VAL_LIMIT} upper {MAX_VAL_LIMIT} - basic.csv'''

specific_name = f'''pop {POPULATION} cy {CYCLES} imp {IMPROVEMENT} min {MIN_VAL}\
    max {MAX_VAL} bottom {MIN_VAL_LIMIT} upper {MAX_VAL_LIMIT} - specific.csv'''


# https://stackoverflow.com/a/179608/5531122
if os.path.isfile(basic_name) and os.path.isfile(specific_name):
    sys.exit('Calculation Already Genarated')

# Calculating the improvement array
if IMPROVEMENT != 1:
    increm = np.linspace(1, IMPROVEMENT, endpoint=True, num=POPULATION)
    np.around(increm, decimals=round(math.log(POPULATION, 10) + 2), out=increm)

# Calculate numpy dtype to be used
if MAX_VAL_LIMIT < 256:
    dtype = np.uint8
elif MAX_VAL_LIMIT < 65536:
    dtype = np.uint16
elif MAX_VAL_LIMIT < 4294967296:
    dtype = np.uint32
else:
    dtype = np.uint64

def print_time_estimate(time_multiplier, time_start: float) -> None:
    '''Calculate time requiered'''

    hours, rem = divmod((time.time() - time_start) * time_multiplier, 3600)
    minutes, seconds = divmod(rem, 60)
    logging.info('Time remaining:\thr:mn:sec')
    logging.info('\t\t\t{:0>2}:{:0>2}:{:0>2}'.format(int(hours), int(minutes),
                                                     int(seconds)))
    

def single_run(POPULATION: int, IMPROVEMENT: float, MIN_VAL: int, MAX_VAL: int,
               MIN_VAL_LIMIT: int, MAX_VAL_LIMIT: int)->tuple[np.ndarray, np.ndarray]:
    '''Generates a single run of the simulation'''
    if MAX_VAL - MIN_VAL == POPULATION:
        logging.debug('MAX_VAL - MIN_VAL == POPULATION')
        single_arr = np.arange(MIN_VAL, MAX_VAL + 1)
    elif MAX_VAL - MIN_VAL > POPULATION:
        logging.debug('MAX_VAL - MIN_VAL > POPULATION')
        single_arr = np.random.randint(MIN_VAL, high=MAX_VAL + 1,
                                       size=POPULATION)
    else:
        logging.debug('MAX_VAL - MIN_VAL < POPULATION')
        single_arr = np.arange(MIN_VAL, MAX_VAL + 1)
        extra = np.random.randint(MIN_VAL, high=MAX_VAL,
                                  size=POPULATION - single_arr.shape[0])
        single_arr = np.concatenate([single_arr, extra])

    np.random.shuffle(single_arr)
    logging.debug(f'single_arr:\n{single_arr}')

    # recalculate for improvement
    if IMPROVEMENT != 1:
        single_arr = single_arr*increm
        if MAX_VAL * IMPROVEMENT > MAX_VAL_LIMIT:
            single_arr[single_arr > MAX_VAL_LIMIT] = MAX_VAL_LIMIT
        if MAX_VAL * IMPROVEMENT < MIN_VAL_LIMIT:
            single_arr[single_arr < MIN_VAL_LIMIT] = MIN_VAL_LIMIT
        np.around(single_arr, decimals=0, out=single_arr)

    avg = np.average(single_arr)
    max = np.max(single_arr)
    last_value = single_arr[-1]
    top_95_value, top_90_value, top_80_value = np.percentile(single_arr,
                                                          [95, 90, 80])
    '''logging.debug(f'\naverage: {avg}'
                  f'\nbest_value: {max}'
                  f'\ntop_95_value: {top_95_value}'
                  f'\ntop_90_value: {top_90_value}'
                  f'\ntop_80_value: {top_80_value}')'''
    iter_basic = np.array([avg, last_value, max, top_95_value, top_90_value,
                          top_80_value],dtype=np.float64)
    # Columns are 'chosen', 'value', 'best', 'top_95', 'top_90', 'top_80'
    iter_results = np.zeros((6, POPULATION),dtype=dtype)

    # Comparing to the best so far
    max_values = np.maximum.accumulate(single_arr)
    
    for i in range(POPULATION):
        # If max value already ocurred skip the comparison
        if max_values[i] >= max:
            iter_results[0][i] = POPULATION
            iter_results[1][i] = last_value
            #print(f'i: {i}, mval: {POPULATION} mval: {last_value}')
        else:
            # Where is the first value higher than the ones until now
            x = np.searchsorted(max_values[i:], max_values[i]+1)
            iter_results[0][i] = i + x
            iter_results[1][i] = single_arr[i + x]
            #print(f'i: {i}, x: {x}, i+x: {i + x} val: {single_arr[i + x]}')

        # Filling target values
        if iter_results[1][i] == max:
            iter_results[2][i] = 1
            iter_results[3][i] = 1
            iter_results[4][i] = 1
            iter_results[5][i] = 1
        elif iter_results[1][i] >= top_95_value:
            iter_results[3][i] = 1
            iter_results[4][i] = 1
            iter_results[5][i] = 1
        elif iter_results[1][i] >= top_90_value:
            iter_results[4][i] = 1
            iter_results[5][i] = 1
        elif iter_results[1][i] >= top_80_value:
            iter_results[5][i] = 1
    logging.debug(f'iter_basic:\t{iter_basic}')
    logging.debug(f'iter_specific:\n{iter_results}')
    return iter_basic, iter_results

def wrapper_function(_):
    # Call the function with the fixed arguments
    return single_run(POPULATION, IMPROVEMENT, MIN_VAL, MAX_VAL,
                      MIN_VAL_LIMIT,MAX_VAL_LIMIT)

def multiprocess_run(iter_function, CYCLES: int, \
                     samples: list) -> tuple[np.ndarray, np.ndarray]:
    '''Takes fuction outputs the tuple'''
    basic = np.zeros(6, dtype=np.float64)
    specific = np.zeros((6, POPULATION), dtype=np.uint64)
    
    for sample in samples:
        time_0 = time.time()
        with mp.Pool() as pool:
            for result in pool.imap(iter_function, range(sample)):
                m_basic, m_specific = result
                basic += m_basic
                specific += m_specific

        # Time it has taken
        print_time_estimate((CYCLES - sample) / sample, time_0)
    
    with mp.Pool() as pool:
        for result in pool.imap(iter_function,
                                range(CYCLES - sum(samples))):
            m_basic, m_specific = result
            basic += m_basic
            specific += m_specific
    
    return basic, specific

# For now script cannot run in if __name__ == "__main__":
time_start = time.time()
basic = np.zeros(6, dtype=np.float64)
specific = np.zeros((6, POPULATION), dtype=np.uint64)

np.set_printoptions(precision=6, suppress=True)

if MULTIPROCESS:
    basic, specific = multiprocess_run(wrapper_function, CYCLES, samples)
        
else:
    for sample in samples:
        for cycle in range(sample):
            s_basic, s_specific = single_run(POPULATION, IMPROVEMENT,
                                             MIN_VAL, MAX_VAL,
                                             MIN_VAL_LIMIT, MAX_VAL_LIMIT)
            basic += s_basic
            specific += s_specific
            
        print_time_estimate((CYCLES - sample) / sample, time_start)

    for cycle in range(CYCLES - sum(samples)):
        s_basic, s_specific = single_run(POPULATION, IMPROVEMENT,
                                         MIN_VAL, MAX_VAL, 
                                         MIN_VAL_LIMIT, MAX_VAL_LIMIT)
        basic += s_basic
        specific += s_specific

# Time Actual
hours, rem = divmod(time.time() - time_start, 3600)
minutes, seconds = divmod(rem, 60)
logging.info('Time Actual:\t\thr:mn:sec')
logging.info('\t\t\t{:0>2}:{:0>2}:{:0>2}'.format(int(hours), int(minutes),
                                                 int(seconds)))

logging.debug(f'Basic data:\t{basic}')
logging.debug(f'Specicic data:\t{specific}\n\n')
basic_final = np.divide(basic, CYCLES)
specific_final = np.divide(specific, CYCLES)
logging.debug('\nAfter dividing by cycles')
logging.debug(f'Basic data final:\t{basic_final}')
logging.debug(f'Specicic data final:\t{specific_final}\n\n')


cols_basic = ['average', 'last_value', 'best_value', 'top_95_value',
              'top_90_value', 'top_80_value']
cols_specific = ['chosen', 'value', 'is_best', 'is_top_95', 'is_top_90',
                 'is_top_80']
# https://stackoverflow.com/a/20168394/5531122
index_basic=pd.RangeIndex(start=1, name='index')
index_specific=pd.RangeIndex(start=1, stop=POPULATION+1, name='index')

df_basic = pd.DataFrame(basic_final[:,None].T, columns=cols_basic,
                        index=index_basic)
df_specific = pd.DataFrame(specific_final.T, columns=cols_specific,
                           index=index_specific)

logging.info(f'\nBasic database\n{df_basic.to_string()}\n')
logging.info(f'\nSpecific database\n{df_specific.to_string()}')

df_basic.to_csv(basic_name, index=True, header=True, sep='\t')
df_specific.to_csv(specific_name, index=True, header=True, sep='\t')
