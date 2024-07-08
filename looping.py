import multiprocessing as mp
import numpy as np

import math
import time
import os
import sys

import pandas as pd

time0 = time.time()


cycles = 100000
# Potential dating partners
population = 1000
# Min value (0 would give nicer averages but no one would date a literal 0)
min_val = 1
# Max value (if there'san improvement it will go up with time)
max_val = 1000

# How much you'll improve until the end (1.0 - no improvement, 1.5 - 50% improvement)
improvement = 1.1
# In case you are or become soo attractive that you can hit the limit
upperCeeling = 2000
# In case it gets only worse
bedrock = 0

# steps taken from max population to zero
# If you don't want to do steps make steps same or bigger than population
step = 10

#For time estimate
first_ten = mp.Value('i', 0)


result_folder = os.getcwd() + '\\Results'

if not os.path.exists(result_folder):
    os.makedirs(result_folder)
os.chdir(result_folder)




#
# Checking inputs
#

if improvement != 1:
    increm = np.linspace(1,improvement,endpoint=True,num=population)
    np.around(increm,decimals=round(math.log(population,10)+2),out=increm)
    #print(increm)
    #print(math.log(population,10))

if upperCeeling <= max_val:
    upperCeeling = max_val


def single_run(k):
    #Get the desired population regardless based on given min and max
    if max_val - min_val == population:
        filler = np.arange(min_val,max_val+1)
    elif max_val - min_val > population:
        filler  = np.arange(min_val,population+min_val)
    else:
        filler = np.arange(min_val,max_val+1)
        extra = np.random.randint(min_val,high=max_val,size=population-filler.shape[0])
        filler = np.concatenate([filler,extra])

    np.random.shuffle(filler)

    # recalculate for improvement
    if improvement != 1:
        filler = filler*increm
        if max_val * improvement > upperCeeling:
            filler[filler > upperCeeling] = upperCeeling
        if max_val * improvement < bedrock:
            filler[filler < bedrock] = bedrock
        np.around(filler,decimals=0,out=filler)
        
    #95%, 90%, 80%
    value_at_95 = (np.amax(filler)-np.amin(filler)+1)*0.95
    value_at_90 = (np.amax(filler)-np.amin(filler)+1)*0.90
    value_at_80 = (np.amax(filler)-np.amin(filler)+1)*0.80
    #print(value_at_95, value_at_90, value_at_80)
    #print('--------------')
    
    #print(filler)
    result  = np.zeros((7,population))
    #Baseline Sum
    result[0] = filler
    #Baseline BEST
    result[1][np.argmax(filler)] = 1

    #Comparing to the best so far
    for i in range(population-1):
        
        # If max value was already seen skip the comparison
        if np.amax(filler[:i+1]) >= np.amax(filler):
            #Score
            result[2][i] += filler[-1]

        else:
            #Where is the first value higher than the ones until now
            x = np.argmax(filler[i:] > np.amax(filler[:i+1])) + i
            #Score
            result[2][i] = filler[x]

            #Filling target values
            if result[2][i] == np.amax(filler):
                # Best
                result[3][i] = 1

            elif result[2][i] >= value_at_95:
                # Top 95
                result[4][i] = 1

            elif result[2][i] >= value_at_90:
                # Top 90
                result[5][i] = 1

            elif result[2][i] >= value_at_80:
                # Top 80
                result[6][i] = 1

    #Evaluating last position
    result[2][-1] = filler[-1]
    if filler[-1] == np.amax(filler):
        result[3][-1] += 1


    if first_ten.value < 10:
        lock = mp.Lock()
        with lock:
            first_ten.value += 1
        #print(first_ten.value)

        if first_ten.value == 10:

            now = time.time() - time0
            estimate = now*cycles/10/6#mp.cpu_count()

            # https://stackoverflow.com/a/27780763/55311220
            #per %
            hours, rem = divmod(now, 3600)
            minutes, seconds = divmod(rem, 60)
            print('Time given:\t\thr:mn:sec.')
            print(10/cycles*100,'% Takes\t'"{:0>2}:{:0>2}:{:05.3f}".format(int(hours),int(minutes),seconds))

            #Untill Ready
            hours, rem = divmod(estimate, 3600)
            minutes, seconds = divmod(rem, 60)
            print('Remaining:\t\t'"{:0>2}:{:0>2}:{:05.3f}".format(int(hours),int(minutes),seconds))

            #https://stackoverflow.com/a/367065/5531122
            sys.stdout.flush()
    return(result)
    
if __name__== "__main__":

    for i in range(1,10001):
        test_name = 'Pop ' + str(population) + ' Cy ' \
                    + str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
                    + ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) \
                    + ' Bottom ' + str(bedrock)+ ' ' + str(i)+'.csv'

        #https://stackoverflow.com/a/179608/5531122
        if os.path.isfile(test_name):
            sys.exit('Already Genarated')
        else:

            time0 = time.time()
            finished  = np.zeros((7,population))

            pool = mp.Pool() #processes=6
            results = pool.map(single_run,range(cycles))
            pool.close()
            pool.join()

            #Time it has taken
            print('------------')
            hours, rem = divmod(time.time()-time0, 3600)
            minutes, seconds = divmod(rem, 60)
            print('Actual:\t\t\t'"{:0>2}:{:0>2}:{:05.3f}".format(int(hours),int(minutes),seconds))
            
            merging = np.zeros((7,population))

            # No Need for shared arrays
            #https://stackoverflow.com/a/44703026/5531122
            #np.set_printoptions(precision=7, suppress = True)
            for a in results:
                merging += a

            merging[0] /= cycles*population
            merging[1] /= cycles
            merging[2] /= cycles*population
            merging[3] /= cycles
            merging[4] /= cycles
            merging[5] /= cycles
            merging[6] /= cycles

            finished = np.transpose(merging)



            names  = ['baseline_total', 'baseline_best', 'total',
            'the_best', 'top_95', 'top_90', 'top_80']

            df = pd.DataFrame(finished, columns=names)
            #https://stackoverflow.com/a/20168394/5531122
            df.index = np.arange(1, len(df)+1)
            df.to_csv(test_name, index=True, header=True, sep=' ')

            del results, merging, finished, df  


