
import random
import copy
import time
import os


cycles = 1000
population = 30
min_val = 1
max_val = 100

improvement = 1.0
upperCeeling =  200

#steps taken from max population to zero
jump = 10

#
# Checking inputs
#

if improvement < 1:
	improvement = 1

if upperCeeling <= max_val:
	upperCeeling = max_val

option_range = max_val - min_val


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

		# Calculating Min and Max values
		maximal_val = int(round(max_val + max_val * (improvement-1) * j / (population-1)))

		if maximal_val > upperCeeling:
			maximal_val = upperCeeling

		a.append(random.randint(min_val, maximal_val))
		j += 1

	startingData[i] = a
	i += 1

time_Zero = time.time()-start_Time
print(time_Zero)


#
# Settting up folder and file names
#

folder_name = 'Dating Pop ' + str(population) + ' Cy ' \
+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling)



name_detail_One = 'Dating Detail One Pop ' + str(population) + ' Cy ' \
+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) + '.txt'

name_detail_Two = 'Dating Detail Two Pop ' + str(population) + ' Cy ' \
+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) + '.txt'

name_detail_Three = 'Dating Detail Three Pop ' + str(population) + ' Cy ' \
+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) + '.txt'



file_summary = 'Dating Summary Pop ' + str(population) + ' Cy  ' \
+ str(cycles) + ' Min ' + str(min_val) + ' Max ' + str(max_val) \
+ ' Imp ' + str(improvement) + ' Upper ' + str(upperCeeling) + '.txt'

folder_location = 'C:\\Users\\Artur\\Desktop\\Coding Files\\Dating Bail Out'


folder = folder_location + '\\' + folder_name

# Creates the folder
if not os.path.exists(folder):
    os.makedirs(folder)


file_detail_One  = folder + '\\' + name_detail_One
file_detail_Two  = folder + '\\' + name_detail_Two
file_detail_Three  = folder + '\\' + name_detail_Three

file_summary_location  = folder + '\\' + file_summary

#
# Iteration over different population sizes and saving results
#

best_Score = [0]*population

Option_Two_Max_Score_Index = [0]*population
Option_Two_Max_Score_Value = [0]*population

Option_Three_Max_Score_Index = [0]*population
Option_Three_Max_Score_Value = [0]*population

Option_Three_Crossing_Index = [0]*population
Option_Three_Crossing_Value = [0]*population

time_One = 0
time_Two = 0
time_Three = 0

time_One_List  = [0]*population
time_Two_List  = [0]*population
time_Three_List  = [0]*population

population_iteration = population
while population_iteration > 0:

	print('----------  ',population_iteration, '  ----------')

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

	time_One_List[population_iteration - 1] = time.time() - time_begining

	print(option_One)


	#
	# Option 2: Settle on someone better than the current one (if unlucky the last one)
	#

	option_Two = [0]*population_iteration
	option_Two_Steps = [0]*population_iteration

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
			option_Two_Steps[n] = option_Two_Steps[n] + p

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

	Option_Two_Max_Score_Index[population_iteration - 1] = option_Two.index(max(option_Two))
	Option_Two_Max_Score_Value[population_iteration - 1] = max(option_Two)

	time_Two_List[population_iteration - 1] = time.time() - time_One - time_begining
	

	#
	# Option 3(main question): Settle with someone better than any until now (if unlucky the last one)
	#

	option_Three = [0]*population_iteration
	option_Three_Steps = [0]*population_iteration

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
			option_Three_Steps[n] = option_Three_Steps[n] + p

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

	Option_Three_Max_Score_Index[population_iteration - 1] = option_Three.index(max(option_Three))
	Option_Three_Max_Score_Value[population_iteration - 1] = max(option_Three)

	z = 0
	while z < population_iteration - 1:
		if option_Two[z] > option_Three[z]:
			
			Option_Three_Crossing_Index[population_iteration - 1] = z
			Option_Three_Crossing_Value[population_iteration - 1] = option_Three[z]
			break
		z += 1

	time_Three_List[population_iteration - 1] = round(time.time() - time_Two - time_begining, 3)


	print('-------------------------------------')
	print('-------------------------------------')
	print('-------------------------------------')


	#
	# Print Summary
	#

	print(option_One)
	print(option_Two)
	print(option_Three)

	print(time_One_List)
	print(time_Two_List)
	print(time_Three_List)

	print(Option_Two_Max_Score_Index)
	print(Option_Two_Max_Score_Value)

	print(Option_Three_Max_Score_Index)
	print(Option_Three_Max_Score_Value)

	#
	# Saving Summary Data
	#
		
	

	population_iteration -= jump

#
	# Deleting empty list elements
	#

	time_One_List = [elem for elem in time_One_List if elem != 0]
	time_Two_List = [elem for elem in time_Two_List if elem != 0]
	time_Three_List = [elem for elem in time_Three_List if elem != 0]


	#
	# Round times and values
	#

	time_One_List = [round(elem,5) for elem in time_One_List]
	time_Two_List = [round(elem,5) for elem in time_Two_List]
	time_Three_List = [round(elem,5) for elem in time_Three_List]

	Option_Two_Max_Score_Value  =  [round(elem,3) for elem in Option_Two_Max_Score_Value]
	Option_Three_Max_Score_Value  = [round(elem,3) for elem in Option_Three_Max_Score_Value]

	option_One = [round(elem,3) for elem in option_One]
	option_Two = [round(elem,3) for elem in option_Two]
	option_Three = [round(elem,3) for elem in option_Three]

	with open(file_summary_location, 'w') as f:
		#Generation speed
		f.write('Generation time\n')
		f.write(str(improvement) + '\n')
		f.write('time\n')
		f.write(str(time_Zero) + '\n')
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