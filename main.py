
import random
import copy
import time
import os

# The higher the value the more presice the values (100000 should be ok)
cycles = 10000
# Potential dating partners
population = 100
# Min value (0 would give nicer averages but no one would date a literal 0)
min_val = 1
# Max value (if there'san improvement it will go up with time)
max_val = 100

# How much you'll improve until the end (1.0 - no improvement, 1.5 - 50% improvement)
improvement = 1.0
# In case you are or become soo attractive that you can hit the limit
upperCeeling = 200

# steps taken from max population to zero
# If you don't want to do steps make steps same or bigger than population
step = 10

#
# Checking inputs
#

# If you'll getting worse with time nearly always the sooner the better
if improvement < 1.0:
	improvement = 1.0

if upperCeeling <= max_val:
	upperCeeling = max_val

if improvement == 1.0:

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