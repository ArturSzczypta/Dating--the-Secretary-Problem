
import random
import copy
import time
import os
import sys

import numpy as np
import itertools
import math
import pandas as pd

#Based on example:
#https://imrankhan17.github.io/pages/Solving%20the%20secretary%20problem%20with%20Python.html

#
# Inputs
#

# The higher the value the more presice the values (100000 should be ok)
cycles = 1000000
# Potential dating partners
population = 10
# Min value (0 would give nicer averages but no one would date a literal 0)
min_val = 1
# Max value (if there'san improvement it will go up with time)
max_val = 100

# How much you'll improve until the end (1.0 - no improvement, 1.5 - 50% improvement)
improvement = 1
# In case you are or become soo attractive that you can hit the limit
upperCeeling = 200
# In case it gets only worse
bedrock = 0

# steps taken from max population to zero
# If you don't want to do steps make steps same or bigger than population
step = 10

result_folder = os.getcwd() + '\\Results'

if not os.path.exists(result_folder):
	os.makedirs(result_folder)

os.chdir(result_folder)


test_name = 'Pop ' + str(population) + ' Cy ' \
+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) \
+ ' Bottom ' + str(bedrock)+ '.csv'

#https://stackoverflow.com/a/179608/5531122
if os.path.isfile(test_name):
	sys.exit('Already Genarated')


#
# Variables
#

filler = np.empty(1)
increm = np.empty(1)
value_at_95 = 0
value_at_90 = 0
value_at_80 = 0

#Baseline
baseline_total = np.zeros(population)
baseline_best = np.zeros(population)


#Results
total = np.zeros(population)
the_best = np.zeros(population)
top_95 = np.zeros(population)
top_90 = np.zeros(population)
top_80 = np.zeros(population)

# Saving
header = np.arange(1,population+1)


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


#
# Generating single array
#

start = time.time()
current  = time.time()
diff = time.time()
printed =  False

#
# Single array
#


for k in range(cycles):
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
		#print(filler)
		filler = filler.astype(int)
		#print(filler)

	#95%, 90%, 80%
	value_at_95 = math.ceil((np.amax(filler)-np.amin(filler))*0.95)
	value_at_90 = math.ceil((np.amax(filler)-np.amin(filler))*0.90)
	value_at_80 = math.ceil((np.amax(filler)-np.amin(filler))*0.80)


	# Baseline 
	np.add(baseline_total,filler, out=baseline_total)
	baseline_best[np.argmax(filler)] += 1

	#Comparing to the best so far

	for i in range(population-1):
		
		# If max value was already seen skip the comparison
		if np.amax(filler[:i+1]) >= np.amax(filler):
			total[i] += filler[-1]

		else:
			x = np.argmax(filler[i:] > np.amax(filler[:i+1])) + i
			total[i] += filler[x]

			#Filling target values
			if filler[x] == np.amax(filler):
				the_best[i] += 1
			elif filler[x] >= value_at_95:
				top_95[i] += 1
			elif filler[x] >= value_at_90:
				top_90[i] += 1
			elif filler[x] >= value_at_80:
				top_80[i] += 1

	#Evaluating last position
	total[-1] += filler[-1]
	if filler[-1] == np.amax(filler):
		the_best[-1] += 1


	#shows progress and time left
	if k % (cycles/100)  == 0  and k/cycles*100 >= 1:
		print(k/cycles*100,' %')

		if printed == False:

			current = time.time()
			diff = (current - start)*(100-(k/cycles*100)/(k/cycles*100))

			# https://stackoverflow.com/a/27780763/55311220
			#per %
			hours, rem = divmod(diff/100, 3600)
			minutes, seconds = divmod(rem, 60)
			print('Time given: hr:min:sec.')
			print('1% Takes '"{:0>2}:{:0>2}:{:05.1f}".format(int(hours),int(minutes),seconds))
			printed = True

			#Untill Ready
			hours, rem = divmod(diff, 3600)
			minutes, seconds = divmod(rem, 60)
			print('Remaining: '"{:0>2}:{:0>2}:{:05.1f}".format(int(hours),int(minutes),seconds))
			printed = True

np.set_printoptions(precision=4, suppress = True)

#
# Saving Data
#

finished = np.column_stack((
	baseline_total/cycles/population,
	baseline_best/cycles, 
	total/cycles/population,
	the_best/cycles,
	top_95/cycles,
	top_90/cycles,
	top_80/cycles))

# https://stackoverflow.com/a/11146434/5531122

names  = ['baseline_total', 'baseline_best', 'total',
	'the_best', 'top_95', 'top_90', 'top_80']

df = pd.DataFrame(finished, columns=names)
#https://stackoverflow.com/a/20168394/5531122
df.index = np.arange(1, len(df)+1)
df.to_csv(test_name, index=True, header=True, sep=' ')	