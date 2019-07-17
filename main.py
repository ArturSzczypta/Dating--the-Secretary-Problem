

import random
import pandas as pd

CYCLES = 10
POPULATION = 10
MIN_VAL = 1
MAX_VAL = 100

improvement = 1
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
	
#print(startingData)

#
# Option 1: Whatif you end with number 1, 2, ...
#

option_One = [None]*POPULATION

k = 0

while k <  CYCLES:
	b = 0
	for col in startingData:
		#print(col[k])
		b = b + col[k]
	option_One[k] = b
	k += 1
#print(option_One, 'before')

option_One[:]  = [x / CYCLES for x in option_One]

#print(option_One, 'after')

#
# Option 2(main question): best after 1, 2, ...
#

option_Two = [None]*POPULATION
secondaryData = startingData
print(secondaryData)


secondaryWaitingTime = x = [[None for _ in range(5)] for _ in range(6)]

m  = 0
while m < POPULATION:
	n = 0
	print(n, m, 'zew')
	while n < CYCLES and m + 1 < POPULATION:
		o = 1

		while m + o < POPULATION:
			while secondaryData[n][m] < secondaryData[n][m + o]:
				o += 1
				print(m + o)
				
			print(m, n, m + o,  secondaryData[n][m], secondaryData[n][m + o])

			secondaryData[n][m] = secondaryData[n][m + o]

			print(m, n, m + o,  secondaryData[n][m], secondaryData[n][m + o])
			


		#print(secondaryData[n][m],secondaryData[n][m + o], 'chosen')
					
		#secondaryData[n][m] = secondaryData[n][m + o]
		#print(o)
		n += 1
	m += 1


m = 0
while m < CYCLES:
	n = 0
	print(m, n, 'zew')

	while n < POPULATION - 2:
		p = 1
		while secondaryData[m][n] >= secondaryData[m][n + p]:
			print(p)
			secondaryData[m][n] = secondaryData[m][n + p]
			if n + p + 1 == POPULATION:
				break
			p += 1
			


	n += 1
