'''Generates a csv file with the results of "the secretary problem"
I decided to leave hyperlinks to the sources'''

import multiprocessing as mp
import numpy as np
import logging
from pathlib import Path
import logging_function as l_f

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
POPULATION = 25
# How many times to run the simulation
CYCLES = 1
# Min value (0 would give nicer averages but no one would date a literal 0)
MIN_VAL = 0
# Max value (if there's an improvement it will go up with time)
MAX_VAL = 20
# How much you'll improve until the end (1.0 - no improvement, 1.5 - 50% impr.)
IMPROVEMENT = 1
# In case it gets only worse
MIN_VAL_LIMIT = 0
# In case you are or become soo attractive that you can hit the limit
MAX_VAL_LIMIT = 107

if MAX_VAL_LIMIT <= MAX_VAL:
    MAX_VAL_LIMIT = MAX_VAL

multiprocess = False

if multiprocess:
    logging.info(f'Number of cores: {mp.cpu_count()}')
    # For time estimate
    first_ten = mp.Value('i', 0)

result_folder = Path.cwd() / 'Results'

if not result_folder.exists():
    result_folder.mkdir(parents=True)
os.chdir(result_folder)

test_name = f'pop {POPULATION} cy {CYCLES} imp {IMPROVEMENT} min {MIN_VAL} ' \
            f'max {MAX_VAL} bottom {MIN_VAL_LIMIT} upper {MAX_VAL_LIMIT}.csv'

# https://stackoverflow.com/a/179608/5531122
if os.path.isfile(test_name):
    sys.exit('Calculation Already Genarated')

# Calculating the improvement
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

def single_run(POPULATION: int, IMPROVEMENT: float, MIN_VAL: int, MAX_VAL: int,
               MIN_VAL_LIMIT: int, MAX_VAL_LIMIT: int) -> np.ndarray:
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
                  f'\nmax: {max}'
                  f'\ntop_95_value: {top_95_value}'
                  f'\ntop_90_value: {top_90_value}'
                  f'\ntop_80_value: {top_80_value}')'''
    basic_data = (avg, last_value, max, top_95_value, top_90_value,
                  top_80_value)
    # Columns are 'chosen', 'value', 'top_95', 'top_90', 'top_80'
    iter_results = np.zeros((5, POPULATION),dtype=dtype)

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
        # Best value
        if iter_results[1][i] == max:
            pass
        elif iter_results[1][i] >= top_95_value:
            iter_results[2][i] = 1
        elif iter_results[1][i] >= top_90_value:
            iter_results[3][i] = 1
        elif iter_results[1][i] >= top_80_value:
            iter_results[4][i] = 1
    logging.debug(f'iter_results:\n{iter_results}')
    print(f'basic_data: {basic_data}')
    return iter_results, basic_data

def multiprocess_run(_) -> np.ndarray:
    ''' Adds time estimation and return calculations from single_run'''
    i_result, b_data = single_run(POPULATION, IMPROVEMENT, MIN_VAL, MAX_VAL,
                        MIN_VAL_LIMIT, MAX_VAL_LIMIT)

    if first_ten.value < 11:
        lock = mp.Lock()
        with lock:
            first_ten.value += 1
    if first_ten.value == 10:

        now = time.time() - time0
        estimate = now*CYCLES/10/mp.cpu_count()

        # https://stackoverflow.com/a/27780763/55311220
        # per %
        hours, rem = divmod(now, 3600)
        minutes, seconds = divmod(rem, 60)
        logging.info('Time given:\thr:mn:sec.')
        logging.info(f'1% ({10/CYCLES*100} Cycles) Takes '
                        "{:0>2}:{:0>2}:{:04.2f}".format(int(hours),
                                                        int(minutes), seconds))
        # Untill Ready
        hours, rem = divmod(estimate, 3600)
        minutes, seconds = divmod(rem, 60)
        logging.info('Remaining: '
                        "{:0>2}:{:0>2}:{:04.2f}".format(int(hours),
                                                        int(minutes), seconds))

        # https://stackoverflow.com/a/367065/5531122
        sys.stdout.flush()
    return 

if __name__ == "__main__":
    time0 = time.time()
    finished = np.zeros((7, POPULATION))
    raw_result = np.zeros((7, POPULATION))
    np.set_printoptions(precision=4, suppress=True)

    if multiprocess:
        pool = mp.Pool()
        results = pool.map(multiprocess_run, range(CYCLES))
        pool.close()
        pool.join()

        # Time it has taken
        hours, rem = divmod(time.time()-time0, 3600)
        minutes, seconds = divmod(rem, 60)
        logging.info('Actual: '
            "{:0>2}:{:0>2}:{:04.2f}".format(int(hours), int(minutes), seconds))
        
        # No Need for shared arrays
        # https://stackoverflow.com/a/44703026/5531122
        np.set_printoptions(precision=4, suppress=True)
        for a in results:
            raw_result += a
    else:
        # Estimate time after 10% is finished
        first_10_cycles = CYCLES//10
        for i in range(CYCLES):
            result = single_run(POPULATION, IMPROVEMENT, MIN_VAL, MAX_VAL,
                                 MIN_VAL_LIMIT, MAX_VAL_LIMIT)
            raw_result += result
        hours, rem = divmod((time.time()-time0)*10, 3600)
        minutes, seconds = divmod(rem, 60)
        logging.info(f'{first_10_cycles:>2d} % - Remaining Time: '
            f'{int(hours):0>2}:{int(minutes):0>2}:{seconds:01.1f}')
        
        # Rest of cycles
        for i in range(CYCLES - first_10_cycles):
            result = single_run(POPULATION, IMPROVEMENT, MIN_VAL, MAX_VAL,
                                 MIN_VAL_LIMIT, MAX_VAL_LIMIT)
            raw_result += result
        
        logging.info('Actual: '
                "{:0>2}:{:0>2}:{:04.2f}".format(int(hours), int(minutes),
                                                seconds))

    raw_result[0] /= CYCLES*POPULATION
    raw_result[1] /= CYCLES
    raw_result[2] /= CYCLES*POPULATION
    raw_result[3] /= CYCLES
    raw_result[4] /= CYCLES
    raw_result[5] /= CYCLES
    raw_result[6] /= CYCLES

    finished = np.transpose(raw_result)

    names = ['baseline_total', 'baseline_best', 'total',
             'the_best', 'top_95', 'top_90', 'top_80']

    df = pd.DataFrame(finished, columns=names)
    # https://stackoverflow.com/a/20168394/5531122
    df.index = np.arange(1, len(df) + 1)
    
    # Line commented, script is not giving right output
    #df.to_csv(test_name, index=True, header=True, sep='\t')
