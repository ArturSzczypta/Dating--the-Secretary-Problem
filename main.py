
import random
import copy
import time
import os

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
cycles = 100
# Potential dating partners
population = 100
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




np.set_printoptions(precision=2, suppress = True)
print(baseline_total/cycles/population*100)
print('-----------------------------')
print(baseline_best/cycles*100)
print('-----------------------------')
print('-----------------------------')
print('-----------------------------')
print('tot: ', total/cycles/population*100)
print('-----------------------------')
print('best: ', the_best/cycles*100)
print('-----------------------------')
print('95: ', top_95/cycles*100)
print('-----------------------------')
print('90: ', top_90/cycles*100)
print('-----------------------------')
print('80: ', top_80/cycles*100)
print('-----------------------------')


#
# Saving Data
#

finished = np.column_stack((baseline_total/cycles/population*100,
	baseline_best/cycles*100, 
	total/cycles/population*100,
	the_best/cycles*100,
	top_95/cycles*100,
	top_90/cycles*100,
	top_80/cycles*100))

# https://stackoverflow.com/a/11146434/5531122

names  = ['baseline_total', 'baseline_best', 'total',
	'the_best', 'top_95', 'top_90', 'top_80']

df = pd.DataFrame(finished, columns=names)
#https://stackoverflow.com/a/20168394/5531122
df.index = np.arange(1, len(df)+1)
df.to_csv('df.csv', index=True, header=True, sep=' ')	
















#
# Option 1 Best than the last one, no going back
#







#baseline = filler.sum(axis=0)/cycles
#print(one_total/np.sum(one_total))















'''

if improvement == 1.0:
	startingData = np.arange









	#
	# Generating Data list
	#

	start_Time = time.time()

	startingData = [None]*cycles

	i = 0

	while i < cycles:

		a = [random.randint(min_val,max_val)]
			
		j = 1
		while len(a) < population:

			# Calculating Max value (if no improvement then it stays the same)
			maximal_val = int(round(max_val + max_val * (improvement-1) * j / (population-1)))

			if maximal_val > upperCeeling:
				maximal_val = upperCeeling

			a.append(random.randint(min_val, maximal_val))
			j += 1

		startingData[i] = a
		i += 1

	time_Zero = time.time()-start_Time
	#print(time_Zero)


	#
	# Settting up main folder and summary name
	#

	folder_location = 'C:\\Users\\Artur\\Desktop\\Coding Files\\Dating Bail Out'


	main_folder_name = 'Dating Pop ' + str(population) + ' Cy ' \
	+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
	+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) + ' Step ' + str(step)

	main_folder = folder_location + '\\' + main_folder_name

	# Creates the folder if doesn't exists
	if not os.path.exists(main_folder):
	    os.makedirs(main_folder)


	file_summary = 'Dating Summary Pop ' + str(population) + ' Cy  ' \
	+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
	+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) + ' Step ' + str(step) + '.txt'

	file_summary_location  = main_folder + '\\' + file_summary


	#
	# Iteration over different population sizes and saving results
	#

	steps_List = []
	option_Two_Steps = []
	option_Three_Steps = []

	Option_Two_Max_Score_Index = []
	Option_Two_Max_Score_Value = []

	Option_Three_Max_Score_Index = []
	Option_Three_Max_Score_Value = []

	Option_Three_Crossing_Index = []
	Option_Three_Crossing_Value = []

	time_One = 0
	time_Two = 0
	time_Three = 0

	time_One_List  = []
	time_Two_List  = []
	time_Three_List  = []

	population_iteration = population
	while population_iteration > 0:

		print('----------  ',population_iteration, '  ----------')

		#
		# Settting up folder and file names
		#

		minor_folder_name = 'Dating Pop ' + str(population_iteration) + ' Cy ' \
		+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
		+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling)

		minor_folder = main_folder + '\\' + minor_folder_name

		# Creates the folder if doesn't exists
		if not os.path.exists(minor_folder):
		    os.makedirs(minor_folder)


		name_detail_One = 'Dating Detail One Pop ' + str(population_iteration) + ' Cy ' \
		+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
		+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) + '.txt'

		name_detail_Two = 'Dating Detail Two Pop ' + str(population_iteration) + ' Cy ' \
		+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
		+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) + '.txt'

		name_detail_Three = 'Dating Detail Three Pop ' + str(population_iteration) + ' Cy ' \
		+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
		+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) + '.txt'


		file_summary = 'Dating Summary Pop ' + str(population_iteration) + ' Cy  ' \
		+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
		+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) + '.txt'


		file_detail_One  = minor_folder + '\\' + name_detail_One
		file_detail_Two  = minor_folder + '\\' + name_detail_Two
		file_detail_Three  = minor_folder + '\\' + name_detail_Three

		time_begining = time.time()


		#
		# Option 1: Average value for each person (if no improvement all should be the same)
		#

		option_One = [0]*population_iteration

		k = 0
		while k <  cycles:
			b = 0
			while b < population_iteration:
				option_One[b] = option_One[b] + startingData[k][b]
				b += 1
			k += 1

		option_One_Sum =sum(option_One)
		# [:] changes the list in question
		option_One[:]  = [x / cycles for x in option_One]

		
		time_One_List.append(time.time() - time_begining)
		print('time_One_List',time_One_List)

		print(option_One, 'OPTION 1')


		#
		# Option 2: Settle on someone better than the current one (if unlucky the last one)
		#

		option_Two = [0]*population_iteration

		#Creating new one
		option_Two_Steps.append(0)

		# deep copy is when you get another list not conected to the last one.
		# without deep copy both list names would point to the same list
		secondaryData = copy.deepcopy(startingData)

		m = 0
		while m < cycles:
			n = 0

			#not touching last one (nowhere to go)
			while n < population_iteration -1:

				p = 1
				while secondaryData[m][n] >= secondaryData[m][n + p]:

					if n + p == population_iteration - 1:
						break
					p += 1
				
				secondaryData[m][n] = secondaryData[m][n + p]
				option_Two_Steps[-1] = option_Two_Steps[-1] + p

				n += 1
			#print(secondaryData[m])
			m += 1

		#Sum all cycles and then do an average
		option_Two = [0]*population_iteration

		k = 0
		while k <  cycles:
			b = 0
			#print(secondaryData[k])
			while b < population_iteration:
				option_Two[b] = option_Two[b] + secondaryData[k][b]
				b += 1
			k += 1

		option_Two_Sum =sum(option_Two)

		option_Two[:]  = [x / cycles for x in option_Two]
		
		print(option_Two, 'OPTION 2')


		# Getting main values of Option two 

		Option_Two_Max_Score_Index.append(option_Two.index(max(option_Two)))
		Option_Two_Max_Score_Value.append(max(option_Two))

		time_Two_List.append(time.time() - time_One - time_begining)
		

		#
		# Option 3(main question): Settle with someone better than any until now (if unlucky the last one)
		#

		option_Three = [0]*population_iteration
		option_Three_Steps.append(0)

		# deep copy is when you get another list not conected to the last one.
		# without deep copy both list names would point to the same list 
		thirdData = copy.deepcopy(startingData)


		m = 0
		while m < cycles:
			n = 0
			q = 0
			maxPop = 0
			#print(startingData[m])
			#not touching last one (nowhere to go)
			while n < population_iteration -1:
				#before looping get highest value until n
				while q <= n:
					if maxPop < startingData[m][q]:
						maxPop = startingData[m][q]
					q += 1
				p = 1
				while maxPop >= startingData[m][n + p]:

					if n + p == population_iteration - 1:
						break
					p += 1

				thirdData[m][n] = thirdData[m][n + p]
				option_Three_Steps[-1] = option_Three_Steps[-1] + p

				#print(m, n, maxPop, p, q, thirdData[m][n], option_Three_Steps, 'after')
				n += 1

			#print(thirdData[m])
			#print('---')
			m += 1
		#print('-------------------------------------')

		#Sum all cycles and then do an average
		k = 0
		while k <  cycles:
			b = 0
			while b < population_iteration:
				option_Three[b] = option_Three[b] + thirdData[k][b]
				b += 1
			k += 1

		option_Three_Sum =sum(option_Three)
		option_Three[:] = [x / cycles for x in option_Three]

		print(option_Three, 'OPTION 3')
		
		# Getting main values of Option three

		Option_Three_Max_Score_Index.append(option_Three.index(max(option_Three)))
		Option_Three_Max_Score_Value.append(max(option_Three))

		z = 0
		while z < population_iteration - 1:
			if option_Two[z] > option_Three[z]:
				
				Option_Three_Crossing_Index.append(z)
				Option_Three_Crossing_Value.append(option_Three[z])
				break
			z += 1

		time_Three_List.append(time.time() - time_Two - time_begining)


		print('-------------------------------------')
		print('-------------------------------------')
		print('-------------------------------------')


		#
		# Print Summary
		#

		print('time_One_List \n',time_One_List)
		print('time_Two_List \n',time_Two_List)
		print('time_Three_List \n',time_Three_List)

		print('Option_Two_Max_Score_Index \n',Option_Two_Max_Score_Index)
		print('Option_Two_Max_Score_Value \n',Option_Two_Max_Score_Value)

		print('Option_Three_Max_Score_Index \n',Option_Three_Max_Score_Index)
		print('Option_Three_Max_Score_Value \n',Option_Three_Max_Score_Value)
	
		#
		# Rounding Detailed Data
		#

		option_One[:] = [round(x, 3) for x in option_One]
		option_Two[:] = [round(x, 3) for x in option_Two]
		option_Three[:] = [round(x, 3) for x in option_Three]


		#
		#Saving Detailed Data
		#

		with open(file_detail_One, 'a') as f:
			f.write(str(option_One) + '\n')
			f.close()

		with open(file_detail_Two, 'a') as f:
			f.write(str(option_Two) + '\n')
			f.close()

		with open(file_detail_Three, 'a') as f:
			f.write(str(option_Three) + '\n')
			f.close()

		steps_List.append(population_iteration)

		population_iteration -= step

else:

	#
	# Generating Data list
	#

	start_Time = time.time()

	startingData = [None]*cycles


	#
	# Iteration over different population sizes and saving results
	#

	steps_List = []
	option_Two_Steps = []
	option_Three_Steps = []

	Option_Two_Max_Score_Index = []
	Option_Two_Max_Score_Value = []

	Option_Three_Max_Score_Index = []
	Option_Three_Max_Score_Value = []

	Option_Three_Crossing_Index = []
	Option_Three_Crossing_Value = []

	time_One = 0
	time_Two = 0
	time_Three = 0

	time_One_List  = []
	time_Two_List  = []
	time_Three_List  = []


	#
	# Settting up main folder and summary name
	#

	folder_location = 'C:\\Users\\Artur\\Desktop\\Coding Files\\Dating Bail Out'


	main_folder_name = 'Dating Pop ' + str(population) + ' Cy ' \
	+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
	+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) + ' Step ' + str(step)

	main_folder = folder_location + '\\' + main_folder_name

	# Creates the folder if doesn't exists
	if not os.path.exists(main_folder):
	    os.makedirs(main_folder)


	file_summary = 'Dating Summary Pop ' + str(population) + ' Cy  ' \
	+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
	+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) + ' Step ' + str(step) + '.txt'

	file_summary_location  = main_folder + '\\' + file_summary

	#iteration over population
	population_iteration = population

	while population_iteration > 0:

		i = 0

		while i < cycles:

			a = [random.randint(min_val,max_val)]
				
			j = 1
			while len(a) < population_iteration:

				# Calculating Max values
				maximal_val = int(round(max_val + max_val * (improvement-1) * j / (population_iteration-1)))

				if maximal_val > upperCeeling:
					maximal_val = upperCeeling

				a.append(random.randint(min_val, maximal_val))
				j += 1

			startingData[i] = a
			i += 1

		time_Zero = time.time()-start_Time
		print(time_Zero)


		print('----------  ',population_iteration, '  ----------')


		#
		# Settting up folder and file names
		#

		minor_folder_name = 'Dating Pop ' + str(population_iteration) + ' Cy ' \
		+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
		+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling)

		minor_folder = main_folder + '\\' + minor_folder_name

		# Creates the folder if doesn't exists
		if not os.path.exists(minor_folder):
		    os.makedirs(minor_folder)


		name_detail_One = 'Dating Detail One Pop ' + str(population_iteration) + ' Cy ' \
		+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
		+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) + '.txt'

		name_detail_Two = 'Dating Detail Two Pop ' + str(population_iteration) + ' Cy ' \
		+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
		+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) + '.txt'

		name_detail_Three = 'Dating Detail Three Pop ' + str(population_iteration) + ' Cy ' \
		+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
		+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) + '.txt'


		file_summary = 'Dating Summary Pop ' + str(population_iteration) + ' Cy  ' \
		+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
		+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) + '.txt'


		file_detail_One  = minor_folder + '\\' + name_detail_One
		file_detail_Two  = minor_folder + '\\' + name_detail_Two
		file_detail_Three  = minor_folder + '\\' + name_detail_Three


		time_begining = time.time()


		#
		# Option 1: Average value for each person (if no improvement all should be the same)
		#

		option_One = [0]*population_iteration

		k = 0
		while k <  cycles:
			b = 0
			while b < population_iteration:
				option_One[b] = option_One[b] + startingData[k][b]
				b += 1
			k += 1

		option_One_Sum =sum(option_One)
		# [:] changes the list in question
		option_One[:]  = [x / cycles for x in option_One]

		
		time_One_List.append(time.time() - time_begining)

		print('time_One_List',time_One_List)

		print(option_One, 'OPTION 1')


		#
		# Option 2: Settle on someone better than the current one (if unlucky the last one)
		#

		option_Two = [0]*population_iteration

		#Creating new one
		option_Two_Steps.append(0)

		# deep copy is when you get another list not conected to the last one.
		# without deep copy both list names would point to the same list
		secondaryData = copy.deepcopy(startingData)

		m = 0
		while m < cycles:
			n = 0

			#not touching last one (nowhere to go)
			while n < population_iteration -1:

				p = 1
				while secondaryData[m][n] >= secondaryData[m][n + p]:

					if n + p == population_iteration - 1:
						break
					p += 1
				
				secondaryData[m][n] = secondaryData[m][n + p]
				option_Two_Steps[-1] = option_Two_Steps[-1] + p

				n += 1
			#print(secondaryData[m])
			m += 1

		#Sum all cycles and then do an average
		option_Two = [0]*population_iteration

		k = 0
		while k <  cycles:
			b = 0
			#print(secondaryData[k])
			while b < population_iteration:
				option_Two[b] = option_Two[b] + secondaryData[k][b]
				b += 1
			k += 1

		option_Two_Sum =sum(option_Two)

		option_Two[:]  = [x / cycles for x in option_Two]
		
		print(option_Two, 'OPTION 2')


		# Getting main values of Option two 

		Option_Two_Max_Score_Index.append(option_Two.index(max(option_Two)))
		Option_Two_Max_Score_Value.append(max(option_Two))

		time_Two_List.append(time.time() - time_One - time_begining)
		

		#
		# Option 3(main question): Settle with someone better than any until now (if unlucky the last one)
		#

		option_Three = [0]*population_iteration
		option_Three_Steps.append(0)

		# deep copy is when you get another list not conected to the last one.
		# without deep copy both list names would point to the same list 
		thirdData = copy.deepcopy(startingData)


		m = 0
		while m < cycles:
			n = 0
			q = 0
			maxPop = 0
			#print(startingData[m])
			#not touching last one (nowhere to go)
			while n < population_iteration -1:
				#before looping get highest value until n
				while q <= n:
					if maxPop < startingData[m][q]:
						maxPop = startingData[m][q]
					q += 1
				p = 1
				while maxPop >= startingData[m][n + p]:

					if n + p == population_iteration - 1:
						break
					p += 1

				thirdData[m][n] = thirdData[m][n + p]
				option_Three_Steps[-1] = option_Three_Steps[-1] + p

				#print(m, n, maxPop, p, q, thirdData[m][n], option_Three_Steps, 'after')
				n += 1

			#print(thirdData[m])
			#print('---')
			m += 1
		#print('-------------------------------------')

		#Sum all cycles and then do an average
		k = 0
		while k <  cycles:
			b = 0
			while b < population_iteration:
				option_Three[b] = option_Three[b] + thirdData[k][b]
				b += 1
			k += 1

		option_Three_Sum =sum(option_Three)
		option_Three[:] = [x / cycles for x in option_Three]

		print(option_Three, 'OPTION 3')
		
		# Getting main values of Option three

		Option_Three_Max_Score_Index.append(option_Three.index(max(option_Three)))
		Option_Three_Max_Score_Value.append(max(option_Three))

		z = 0
		while z < population_iteration - 1:
			if option_Two[z] > option_Three[z]:
				
				Option_Three_Crossing_Index.append(z)
				Option_Three_Crossing_Value.append(option_Three[z])
				break
			z += 1

		time_Three_List.append(time.time() - time_Two - time_begining)


		print('-------------------------------------')
		print('-------------------------------------')
		print('-------------------------------------')


		#
		# Print Summary
		#

		print('time_One_List \n',time_One_List)
		print('time_Two_List \n',time_Two_List)
		print('time_Three_List \n',time_Three_List)

		print('Option_Two_Max_Score_Index \n',Option_Two_Max_Score_Index)
		print('Option_Two_Max_Score_Value \n',Option_Two_Max_Score_Value)

		print('Option_Three_Max_Score_Index \n',Option_Three_Max_Score_Index)
		print('Option_Three_Max_Score_Value \n',Option_Three_Max_Score_Value)


		#
		# Rounding Detailed Data
		#

		option_One[:] = [round(x, 3) for x in option_One]
		option_Two[:] = [round(x, 3) for x in option_Two]
		option_Three[:] = [round(x, 3) for x in option_Three]


		#
		#Saving Detailed Data
		#

		with open(file_detail_One, 'a') as f:
			f.write(str(option_One) + '\n')
			f.close()

		with open(file_detail_Two, 'a') as f:
			f.write(str(option_Two) + '\n')
			f.close()

		with open(file_detail_Three, 'a') as f:
			f.write(str(option_Three) + '\n')
			f.close()

		steps_List.append(population_iteration)

		population_iteration -= step


#
# Round times and values
#

time_One_List = [round(elem,5) for elem in time_One_List]
time_Two_List = [round(elem,5) for elem in time_Two_List]
time_Three_List = [round(elem,5) for elem in time_Three_List]

Option_Two_Max_Score_Value  =  [round(elem,3) for elem in Option_Two_Max_Score_Value]
Option_Three_Max_Score_Value  = [round(elem,3) for elem in Option_Three_Max_Score_Value]

with open(file_summary_location, 'w') as f:
	#Generation itself
	f.write('Generation time\n')
	f.write(str(improvement) + '\n')
	f.write('time\n')
	f.write(str(time_Zero) + '\n')
	f.write('\n')
	f.write('steps\n')
	f.write(str(steps_List) + '\n')
	f.write('\n')

	#Option One
	f.write('Option One\n')
	f.write('time\n')
	f.write(str(time_One_List) + '\n')
	f.write('\n')

	#Option Two
	f.write('Option Two\n')
	f.write('time\n')
	f.write(str(time_Two_List) + '\n')
	f.write('steps\n')
	f.write(str(option_Two_Steps) + '\n')
	f.write('Max Score Index\n')
	f.write(str(Option_Two_Max_Score_Index) + '\n')
	f.write('Max Score Value\n')
	f.write(str(Option_Two_Max_Score_Value) + '\n')
	f.write('\n')

	#Option Three
	f.write('Option Three\n')
	f.write('time\n')
	f.write(str(time_Three_List) + '\n')
	f.write('steps\n')
	f.write(str(option_Three_Steps) + '\n')
	f.write('Max Score Index\n')
	f.write(str(Option_Three_Max_Score_Index) + '\n')
	f.write('Max Score Value\n')
	f.write(str(Option_Three_Max_Score_Value) + '\n')
	f.write('Crossing Index\n')
	f.write(str(Option_Three_Crossing_Index) + '\n')
	f.write('Crossing Value\n')
	f.write(str(Option_Three_Crossing_Value) + '\n')
	f.close()
'''