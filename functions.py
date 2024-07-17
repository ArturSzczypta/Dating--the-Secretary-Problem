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


# How many times to run the simulation
CYCLES = 2000
# Potential dating partners
POPULATION = 100
# Min value (0 would give nicer averages but no one would date a literal 0)
MIN_VAL = 1
# Max value (if there's an improvement it will go up with time)
MAX_VAL = 200
# How much you'll improve until the end (1.0 - no improvement, 1.5 - 50% impr.)
IMPROVEMENT = 1.9
# In case it gets only worse
MIN_VAL_LIMIT = 0
# In case you are or become soo attractive that you can hit the limit
MAX_VAL_LIMIT = 200
if MAX_VAL_LIMIT <= MAX_VAL:
    MAX_VAL_LIMIT = MAX_VAL

multiprocess =  True
if multiprocess:
    logging.info(f'Number of cores: {mp.cpu_count()}')
    # For time estimate
    first_ten = mp.Value('i', 0)


result_folder = Path.cwd() / 'Results'

if not result_folder.exists():
    result_folder.mkdir(parents=True)
os.chdir(result_folder)

test_name = f'pop {POPULATION} cy {CYCLES} imp {IMPROVEMENT} min {MIN_VAL} ' \
            f'max {MAX_VAL} upper {MAX_VAL_LIMIT} bottom {MIN_VAL_LIMIT}.csv'

# https://stackoverflow.com/a/179608/5531122
if os.path.isfile(test_name):
    sys.exit('Already Genarated')

# Calculating the improvement
if IMPROVEMENT != 1:
    increm = np.linspace(1, IMPROVEMENT, endpoint=True, num=POPULATION)
    np.around(increm, decimals=round(math.log(POPULATION, 10) + 2), out=increm)

def single_run(POPULATION: int, IMPROVEMENT: float, MIN_VAL: int, MAX_VAL: int,
               MIN_VAL_LIMIT: int, MAX_VAL_LIMIT: int) -> np.ndarray:
    '''Generates a single run of the simulation'''
    if MAX_VAL - MIN_VAL == POPULATION:
        filler = np.arange(MIN_VAL, MAX_VAL + 1)
    elif MAX_VAL - MIN_VAL > POPULATION:
        filler = np.arange(MIN_VAL, POPULATION + MIN_VAL)
    else:
        filler = np.arange(MIN_VAL, MAX_VAL + 1)
        extra = np.random.randint(MIN_VAL, high=MAX_VAL,
                                  size=POPULATION-filler.shape[0])
        filler = np.concatenate([filler, extra])

    np.random.shuffle(filler)

    # recalculate for improvement
    if IMPROVEMENT != 1:
        filler = filler*increm
        if MAX_VAL * IMPROVEMENT > MAX_VAL_LIMIT:
            filler[filler > MAX_VAL_LIMIT] = MAX_VAL_LIMIT
        if MAX_VAL * IMPROVEMENT < MIN_VAL_LIMIT:
            filler[filler < MIN_VAL_LIMIT] = MIN_VAL_LIMIT
        np.around(filler, decimals=0, out=filler)


    # Values for Top 95%, 90%, 80% of partners
    range_size = np.amax(filler) - np.amin(filler) + 1
    top_95_value, top_90_value, top_80_value = np.percentile(range_size,
                                                          [95, 90, 80])

    result = np.zeros((7, POPULATION))
    # Baseline Sum
    result[0] = filler
    # Baseline BEST
    result[1][np.argmax(filler)] = 1

    # Comparing to the best so far
    max_values = np.maximum.accumulate(filler)
    for i in range(POPULATION - 1):
        current_max = max_values[i]
        # If max value was already seen skip the comparison
        if np.amax(filler[:i+1]) >= np.amax(filler):
            # Score
            result[2][i] += filler[-1]
        else:
            # Where is the first value higher than the ones until now
            x = i + np.argmax(filler[i:] > current_max)
            # Score
            result[2][i] += filler[x]

            # Filling target values
            # Best value
            if result[2][i] == np.amax(filler):
                result[3][i] = 1

            elif result[2][i] >= top_95_value:
                result[4][i] = 1

            elif result[2][i] >= top_90_value:
                result[5][i] = 1

            elif result[2][i] >= top_80_value:
                result[6][i] = 1

    # Evaluating last position
    result[2][-1] = filler[-1]
    if filler[-1] == np.amax(filler):
        result[3][-1] += 1
    return result

def multiprocess_run(_) -> np.ndarray:
    ''' Adds time estimation and return calculations from single_run'''
    result = single_run(POPULATION, IMPROVEMENT, MIN_VAL, MAX_VAL,
                        MIN_VAL_LIMIT, MAX_VAL_LIMIT)

    if first_ten.value < 10:
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
    return result

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
        cycles_first_10 = CYCLES//10
        for i in range(CYCLES):
            results = single_run(POPULATION, IMPROVEMENT, MIN_VAL, MAX_VAL,
                                 MIN_VAL_LIMIT, MAX_VAL_LIMIT)
            raw_result += results
        hours, rem = divmod((time.time()-time0)*10, 3600)
        minutes, seconds = divmod(rem, 60)
        logging.info(f'{cycles_first_10:>2d} %  -  Remaining Time: '
            f'{int(hours):0>2}:{int(minutes):0>2}:{seconds:01.1f}')
        
        for i in range(CYCLES - cycles_first_10):
            results = single_run(POPULATION, IMPROVEMENT, MIN_VAL, MAX_VAL,
                                 MIN_VAL_LIMIT, MAX_VAL_LIMIT)
            raw_result += results
        
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
    df.to_csv(test_name, index=True, header=True, sep='\t')
