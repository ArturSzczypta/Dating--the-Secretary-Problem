
<<<<<<< Updated upstream
=======
import random
import copy
import time
import os.path

>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
# Option 1: Whatif you end with number 1, 2, ...
=======
# Settting up file
#
folder_name = 'Dating Pop ' + str(population) + ' Cy  ' \
+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling)


name_detail_One = 'Dating Detail One Pop ' + str(population) + ' Cy  ' \
+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) + '.txt'

name_detail_Two = 'Dating Detail Two Pop ' + str(population) + ' Cy  ' \
+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) + '.txt'

name_detail_Three = 'Dating Detail Three Pop ' + str(population) + ' Cy  ' \
+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) + '.txt'


file_summary = 'Dating Summary Pop ' + str(population) + ' Cy  ' \
+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) + '.txt'

folder_location = 'C:\\Users\\Artur\\Desktop\\Coding Files\\Dating Bail Out'

folder = folder_location + '\\' + folder_name


file_detail_One  = folder + '\\' + name_detail_One
file_detail_Two  = folder + '\\' + name_detail_Two
file_detail_Three  = folder + '\\' + name_detail_Three

file_summary_location  = folder + '\\' + file_summary



#
# Iteration over different population sizes and saving results
>>>>>>> Stashed changes
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
			
<<<<<<< Updated upstream
=======
			Option_Three_Crossing_Index[population_iteration - 1] = z
			Option_Three_Crossing_Value[population_iteration - 1] = option_Three[z]
			break
		z += 1

	time_Three_List[population_iteration - 1] = time.time() - time_Two - time_begining

	print('CROSSING', Option_Three_Crossing_Index[population_iteration - 1], Option_Three_Crossing_Value[population_iteration - 1])

	print('-------------------------------------')
	print('-------------------------------------')
	print('-------------------------------------')

	print(time_One_List)
	print(time_Two_List)
	print(time_Three_List)

	f  = open('file_detail_One',  'w')
	f.write(option_One + '\n')
	f.close()

	f  = open('file_detail_Two',  'w')
	f.write(option_Two + '\n')
	f.close()

	f  = open('file_detail_Three',  'w')
	f.write(option_Three + '\n')
	f.close()


>>>>>>> Stashed changes


<<<<<<< Updated upstream
	n += 1
=======
print(Option_Three_Max_Score_Index)
print(Option_Three_Max_Score_Value)

#
# Saving Data
#

with open(file_summary, 'w') as f:
	#Option One
	f.write('Option One\n')
	f.write(time_One_List + '\n')
	f.write('\n')

	f.write('Option Two\n')
	f.write(time_Two_List + '\n')
	f.write(option_Two_Steps + '\n')
	f.write(Option_Two_Max_Score_Index + '\n')
	f.write(Option_Two_Max_Score_Value + '\n')
	f.write('\n')

	f.write('Option Three\n')
	f.write(time_Three_List + '\n')
	f.write(option_Three_Steps + '\n')
	f.write(Option_Three_Max_Score_Index + '\n')
	f.write(Option_Three_Max_Score_Value + '\n')
>>>>>>> Stashed changes
