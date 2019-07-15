

import random
import pandas as pd

CYCLES = 10
POPULATION = 10
MIN_VAL = 1
MAX_VAL = 100

improvement = 1.5
upperCeeling =  200

if improvement < 1:
	improvement = 1

if upperCeeling <= MAX_VAL:
	upperCeeling = MAX_VAL

#
# Generating Data list
#

#To start with consequtive numbers:

#startingData = list(range(1,POPULATION+2))
#startingData[0] = list(range(CYCLES+1))
#i = 1
#while i <= POPULATION:

startingData = [None]*CYCLES
i = 0

while i < CYCLES:

	a = [random.randint(MIN_VAL,MAX_VAL)]
		
	j = 1
	while len(a) < POPULATION:

		# Calculating Min and Max values
		maximalVal = int(round(MAX_VAL + MAX_VAL * (improvement-1) * j / (POPULATION-1)))
		
		if maximalVal > upperCeeling:
			maximalVal = upperCeeling

		a.append(random.randint(MIN_VAL,maximalVal))
		j += 1
	
	#Dividing by max value keeping oldname. If there's new name don't type in [:]
	divider = max(a)
	if divider > MAX_VAL:
		divider = MAX_VAL

	a[:] = [x / divider for x in a]

	startingData[i] = a
	i += 1
	
print(startingData)

#
# Option 1: Whatif you end with number 1, 2, ...
#

Option_One = [None]*POPULATION
print(startingData[[0]])