
import random
import copy
import time
import os
import csv

# The higher the value the more presice the values (100000 should be ok)
cycles = 10000
# Potential dating partners
population = 100
# Min value (0 would give nicer averages but no one would date a literal 0)
min_val = 0
# Max value (if there'san improvement it will go up with time)
max_val = 99

# How much you'll improve until the end (1.0 - no improvement, 1.5 - 50% improvement)
improvement = 1
# In case you are or become soo attractive that you can hit the limit
upperCeeling = 199

# steps taken from max population to zero
# If you don't want to do steps make steps same or bigger than population
step = 100


#
# Generating Data list
#

start_Time = time.time()

startingData = [None]*cycles

starting_list = list(range(min_val, max_val+1))
#print(starting_list)

starting_length = len(starting_list)

if population >= starting_length:
	for i in range(cycles):
		# deep copy is when you get another list not conected to the last one.
		# without deep copy both list names would point to the same list
		startingData[i] = copy.deepcopy(starting_list)

	while population > starting_length:
		for i in range(cycles):
			startingData[i].append(random.randint(min_val, max_val+1))
		starting_length += 1

if population < starting_length:
	for i in range(cycles):
		startingData[i] = random.sample(range(min_val, max_val+1), population)

for i in range(cycles):
		random.shuffle(startingData[i])


'''
for i in startingData:
	for j in i:
		print('{:4d}'.format(j),end ='')
	print()

'''


#multplitication = [None]*population

#find all max values [i for i, x in enumerate(a) if x == max(a)]

if improvement != 1.0:
	change  = (improvement-1) / population
	for i in range(cycles):
		for j in range(population):
			k = round(startingData[i][j] * (1+change*(j+1)))
			#print(j+1,round(1+change*(j+1),2), '   \t', startingData[i][j],k,end='   ')
			#multplitication[j] = round(1+change*(j+1),2)
			if k > upperCeeling:
				startingData[i][j] = upperCeeling
			elif k < min_val:
				startingData[i][j] = min_val
			else:
				startingData[i][j] = k
			#print(startingData[i][j])
		#print()

# Finding max values, if longer lists please see @martineau
# https://stackoverflow.com/questions/3989016/how-to-find-all-positions-of-the-maximum-value-in-a-list
max_cycle_ind = [0]*cycles
for i in range(cycles):
	m_in = startingData[i].index(max(startingData[i]))
	m = startingData[i][m_in]
	for j in range(m_in, population) :
		if  startingData[i][j] == m:
			max_cycle_ind[i] = j


'''
for i in startingData:
	for j in i:
		print('{:4d}'.format(j),end ='')
	print()

for j in max_cycle_ind:
		print('{:4d}'.format(j),end ='')
print()
'''

time_Zero = time.time()-start_Time


#
# Settting up main folder and summary file
#

folder_location = 'C:\\Users\\Artur\\Desktop\\Coding Files\\Dating Bail Out'

folder_name = 'Dating Pop ' + str(population) + ' Cy ' \
+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) \
+ ' Step ' + str(step)

this_folder = folder_location + '\\' + folder_name

# Creates the folder if doesn't exists
if not os.path.exists(this_folder):
    os.makedirs(this_folder)

file_summary = 'Dating Summary Pop ' + str(population) + ' Cy  ' \
+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) \
+ ' Step ' + str(step) + '.txt'

summary  = this_folder + '\\' + file_summary


#
# Iteration over different population sizes and saving results
#

steps_List = []
option_Two_Steps = []
option_Three_Steps = []

option_Two_Max_Score_Index = []
option_Two_Max_Score_Value = []
option_Two_Best_Score_Prop = []

option_Three_Max_Score_Index = []
option_Three_Max_Score_Value = []
option_Three_Best_Score_Prop = []

option_Three_Crossing_Index = 0
option_Three_Crossing_Value = 0

best_Crossing_Index  = 0
best_Crossing_Value = 0

time_One = 0
time_Two = 0
time_Three = 0

time_One_List  = []
time_Two_List  = []
time_Three_List  = []


population_iteration = population
while population_iteration > 0:
	
	print(str(population_iteration).center(20,'-'))

	steps_List.append(population_iteration)

	#
	# Settting up folder and file names
	#


	detail_name = 'Dating Detail ' + str(population_iteration) + ' Cy ' \
	+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
	+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) \
	+ ' Step ' + str(step) + '.csv'

	detail  = this_folder + '\\' + detail_name
	
	
	time_begining = time.time()


	#
	# Option 1: Average value for each person (if no improvement all should be the same)
	#

	# Compress all interations into one  list
	def main_compressor(nested_list, decimals = 2):
		return [round(sum(x)/cycles,decimals) for x in zip(*nested_list)]

	option_One = main_compressor(startingData)
	print('OPTION 1', '\n', option_One)


	def save_data(file_d, list_name, size):
		with open(file_d, 'a', newline = '') as f:
			writer = csv.writer(f)
			writer.writerow(list_name[:size])
	def free_memory(list_name):
		list_name =  None
		del list_name


	print(option_One[:population_iteration])
	#save_data(detail, option_One, population_iteration)
	'''with open(detail, 'a', newline = '') as f:
						writer = csv.writer(f)
						writer.writerow(option_One[:population_iteration])
			
				free_memory(option_One)'''

	time_One_List.append(time.time() - time_begining)
	#print('time_One_List',time_One_List)


	#
	# Option 2: Settle on someone better than the current one (if unlucky the last one)
	#


	#Creating new one
	option_Two_Steps.append(0)

	secondaryData = copy.deepcopy(startingData)

	for m in range(cycles):

		#not touching last one (nowhere to go)
		
		for n in range(population_iteration-1):
			
			if n == max_cycle_ind[m]:
				secondaryData[m][n] = startingData[m][population_iteration-1]
				option_Two_Steps[-1] += population_iteration-1 - n
				
			else:
				p = 1
				while startingData[m][n] >= startingData[m][n + p]:
					if n + p == population_iteration - 1:
						break
					p += 1

				secondaryData[m][n] = startingData[m][n + p]
				#print(n,p)
				option_Two_Steps[-1] += p
		#print(secondaryData[m])
		


	#Sum all cycles and then do an average
	option_Two = main_compressor(secondaryData)

	#How often fo you get the best value
	def best_score_finder(nested_list, decimals = 4):
		result = [0]*population_iteration
		for i in range(cycles):
			for j in range(population_iteration):
				if nested_list[i][j] == max(nested_list[i]):
					result[j] += 1
		return [round(x*100/sum(result),decimals) for x in result]

	option_Two_Best_Score_Prop = best_score_finder(secondaryData)
	

	free_memory(secondaryData)
	save_data(detail, option_Two, population_iteration)
	print('OPTION 2', '\n', option_Two)
	print('------------')
	print()
	print('max_perc_2',option_Two_Best_Score_Prop)
	print(sum(option_Two_Best_Score_Prop))
	print(option_Two_Best_Score_Prop.index(max(option_Two_Best_Score_Prop)))
	print()
	print('------------')

	# Getting main values of Option Two
	option_Two_Max_Score_Index.append(option_Two.index(max(option_Two)))
	option_Two_Max_Score_Value.append(max(option_Two))

	time_Two_List.append(time.time() - time_One - time_begining)
	
	
	#
	# Option 3(main question): Settle with someone better than any until now (if unlucky the last one)
	#

	
	option_Three_Steps.append(0)

	thirdData = copy.deepcopy(startingData)


	
	for m in range(cycles):
		q = 0
		maxPop = 0
		#print(startingData[m])
		#not touching last one (nowhere to go)
		for n in range(population_iteration-1):

			if n >= max_cycle_ind[m]:
				thirdData[m][n] = startingData[m][population_iteration-1]
				option_Three_Steps[-1] += population_iteration-1 - n
			else:

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

				thirdData[m][n] = startingData[m][n + p]
				option_Three_Steps[-1] += p

				#print(m, n, maxPop, p, q, thirdData[m][n], option_Three_Steps, 'after')

	'''for i in thirdData:
						for j in i:
							print('{:4d}'.format(j),end ='')
						print()'''


	#Sum all cycles and then do an average
	#print(thirdData)
	option_Three = main_compressor(thirdData)

	option_Three_Best_Score_Prop = best_score_finder(thirdData)

	free_memory(thirdData)
	save_data(detail, option_Three, population_iteration)
	print('OPTION 3', '\n', option_Three)

	print('------------')
	print()
	print('max_perc_3',option_Three_Best_Score_Prop)
	print(sum(option_Three_Best_Score_Prop))
	print(option_Three_Best_Score_Prop.index(max(option_Three_Best_Score_Prop)))
	print()
	print('------------')


	
	# Getting main values of Option Three

	option_Three_Max_Score_Index.append(option_Three.index(max(option_Three)))
	option_Three_Max_Score_Value.append(max(option_Three))

	time_Three_List.append(time.time() - time_Two - time_begining)

	z = 0
	while z < population_iteration - 1:
		if option_Two[z] > option_Three[z]:
			
			option_Three_Crossing_Index =z
			option_Three_Crossing_Value= option_Three[z]
			break
		z += 1

	z = 0
	while z < population_iteration - 1:
		if option_Two_Best_Score_Prop[z] > option_Three_Best_Score_Prop[z]:
			
			best_Crossing_Index = z
			best_Crossing_Value = option_Three_Best_Score_Prop[z]
			break
		z += 1
	print('crossing', best_Crossing_Index, best_Crossing_Value)

	print('-------------------------------------')
	print('-------------------------------------')
	print('-------------------------------------')


	#
	# Print Summary
	#

	print('time_One_List \n',time_One_List)
	print('time_Two_List \n',time_Two_List)
	print('time_Three_List \n',time_Three_List)
	
	print('Option_Two_Max_Score_Index \n',option_Two_Max_Score_Index)
	print('Option_Two_Max_Score_Value \n',option_Two_Max_Score_Value)

	print('Option_Three_Max_Score_Index \n',option_Three_Max_Score_Index)
	print('Option_Three_Max_Score_Value \n',option_Three_Max_Score_Value)

	
	population_iteration -= step
	#print(population_iteration, step, population_iteration - step)




#
# Round times and values
#

time_One_List = [round(elem,5) for elem in time_One_List]
time_Two_List = [round(elem,5) for elem in time_Two_List]
time_Three_List = [round(elem,5) for elem in time_Three_List]

option_Two_Max_Score_Value  =  [round(elem,3) for elem in option_Two_Max_Score_Value]
option_Three_Max_Score_Value  = [round(elem,3) for elem in option_Three_Max_Score_Value]

with open(summary, 'w') as f:
	#Generation itself
	f.write('Generation time\n')
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
	f.write(str(option_Two_Max_Score_Index) + '\n')
	f.write('Max Score Value\n')
	f.write(str(option_Two_Max_Score_Value) + '\n')
	f.write('Best Score Propability\n')
	f.write(str(option_Two_Best_Score_Prop) + '\n')


	f.write('\n')

	#Option Three
	f.write('Option Three\n')
	f.write('time\n')
	f.write(str(time_Three_List) + '\n')
	f.write('steps\n')
	f.write(str(option_Three_Steps) + '\n')
	f.write('Max Score Index\n')
	f.write(str(option_Three_Max_Score_Index) + '\n')
	f.write('Max Score Value\n')
	f.write(str(option_Three_Max_Score_Value) + '\n')
	f.write('Best Score Propability\n')
	f.write(str(option_Three_Best_Score_Prop) + '\n')

	f.write('Crossing Index\n')
	f.write(str(best_Crossing_Index) + '\n')
	f.write('Crossing Value\n')
	f.write(str(best_Crossing_Value) + '\n')

	f.close()
