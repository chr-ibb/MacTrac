"""
Learned/Developed:
-used enumerate to for-loop through a list and have the item in the list AND the index
	-used enumerate to print out a list of food items with corresponding index so that user can choose by index
-used deque, a container that pops from the begining better than lists
	-used deque to store all the data from a txt file, popped from the left side as i looped through the deque
	-in later versions, saving to a txt file was replaced with use of lib.pickle
-opening, reading, writing files
	-used to save/load macro data to/from a .txt file
	-used to save/load macro data to/from a binary .pickle file
	-learned a bit about "race conditions" and how to avoid them. basically I dont want to check if a file exists, and then either
		create the file or open it, because in between those two actions the file could be created or deleted. 
-timing runtime of different parts of program using time.clock(), which on windows is more accurate than time.time()
-used lib.pickle to serealize and store macro data, instead of saving to a txt file like before
-used "with as" statement for opening and closing a file
-dictionaries and for loops
-lib.datetime
	-printing different dates
	-adding or subtracting days using datetime.timedelta(n)
	-checking time difference between dates, datetime.timedelta(n).days
-to sort lists, and how to use a sorted list in conjunction with a dictionary
-to use continue and break in a loop
-catching multiple errors in one except line, using a tuple and "as e" after
-creating and using new data types
"""


import datetime
import time
import os
import msvcrt
# from collections import deque # used in older version for loading/saving the data
import pickle

title = ''
title += "  #   #               #######                \n"
title += " # # # #                 #                   \n"
title += " # # # #    ##    ###    #   # ###  ##    ###\n"
title += "#   #   #  #  #  #       #   ##    #  #  #   \n"
title += "#   #   #  #  #  #       #   #     #  #  #   \n"
title += "#   #   #   ## #  ###    #   #      ## #  ###\n"

def MacTrac():
	"""
	Main function. Loads saved data, then runs through the main loop
	where the user can view, add, and remove macro nutrients
	"""
	clear_screen()
	print(title)
	
	days = load_macros()
	wait_sec(1)
	
	view_day = datetime.date.today() # sets the first day to display
	while True: #main loop
		clear_screen()
		print(title)

		view_macro(days, view_day)

		print("\nAdd / Remove macro here: (E) / (R)    Previous / Following day: (A) / (D)    Select by date: (S)    Save and Exit: (Q)")
		choice = msvcrt.getwch() # get input from keyboard
		if choice == 'e' or choice == 'E':
			add_macro(days, view_day)
		elif choice == 'r' or choice == 'R':
			remove_macro(days, view_day)
		elif choice == 'a' or choice == 'A':
			view_day -= datetime.timedelta(1)
		elif choice == 'd' or choice == 'D':
			view_day += datetime.timedelta(1)
		elif choice == 's' or choice == 'S':
			view_day = pick_day()
		elif choice == 'q' or choice == 'Q':
			save_macros(days)
			wait_sec(2)
			break
		else:
			print("Please enter the letters E, A, D, S, or Q")
			wait_sec(1)


def view_macro(days, date):
	"""
	Takes in a dictionary of DAYS, and a DATE to view
	prints out the date and all of the saved macros for that day
	"""
	print(date.strftime("%A, %B %d, %Y")) # print the day, American style
	if date == datetime.date.today():
		print('Today')
	elif date == datetime.date.today() - datetime.timedelta(1):
		print('Yesterday')
	elif date == datetime.date.today() + datetime.timedelta(1):
		print('Tomorrow')
	elif date < datetime.date.today():
		print('{0} days ago'.format((datetime.date.today() - date).days))
	elif date > datetime.date.today():
		print('{0} days from now'.format((date - datetime.date.today()).days))

	if date in days:
		day = days[date]
		print("\nTotal: {0} Calories, {1}g Protein\n".format(day.calories, day.protein))
		for item in day.food:
			print(item)
	else:
		print("\nTotal: 0 calories, 0g protein\n")


def add_macro(days, date):
	"""
	Takes in a dictionary of DAYS, and a DATE to add macro to.
	Prompts user for a Name and amount of Calories and Protein.
	Adds the Day to DAYS if it's not there, and adds a Food to that Day
	"""
	clear_screen()
	print(title)
	view_macro(days, date)

	try:
		name = input("\nName: ")
		cal = int(input("Calories: "))
		pro = int(input("Protein(g): "))
	except ValueError:
		print("Calories and Protein must be numbers")
		wait_sec(1)
		return

	if date not in days:
		days[date] = Day(date)
	days[date].add_food(name, cal, pro)


def remove_macro(days, date):
	"""
	Takes in a dictionary of DAYS and a DATE to remove a macro from.
	Prints all saved macros for that Day, user selects one to remove by element number
	"""
	if date in days and days[date].food:
		while True:
			clear_screen()
			print(title)
			for i, item in enumerate(days[date].food): # prints the element number next to the food item
				print(i, item)
			cancel = len(days[date].food)
			print(cancel, "Cancel")

			try:
				to_remove = int(input("Remove which? Enter number: "))
				if to_remove == cancel: break
				days[date].remove_food(to_remove)
				break
			except (TypeError, ValueError) as e:
				print('Enter an integer')
				wait_sec(1)
				continue
			except IndexError:
				print('Number too large or too small')
				wait_sec(1)
				continue
	else:
		print("nothing to remove...")
		wait_sec(1)


def pick_day():
	"""
	Allows the user to select a Day by inputting the date, rather than by scrolling through days.
	Prompts user for year, month, and day, returns appropriate Date
	"""
	while True:
		clear_screen()
		print(title)

		try:
			year = int(input("year: "))
			month = int(input("month: "))
			day = int(input("day: "))
		except ValueError:
			continue

		try:
			return datetime.date(year, month, day)
		except (ValueError, OverflowError) as e:
			continue


def load_macros():
	"""
	Loads and returns a dictionary called days from MacFile.pickle, if the file exists
	"""
	print("Loading saved macros...\n")
	now = time.perf_counter()
	try:
		with open('MacFile.pickle', 'rb') as f:
			days = pickle.load(f)
		passed = time.perf_counter() - now
		print("Finished loading! Loading took {0} seconds\n".format(passed))
		return days
	except FileNotFoundError:
		print("No macros saved yet, welcome to MacTrac!")
		return {}


def save_macros(days):
	"""
	Saves the dictionary DAYS, which contains all of the macro data, to MacFile.pickle
	"""
	print("Saving macros...")
	with open ('MacFile.pickle', 'wb') as f:
		pickle.dump(days, f)
	print("Finished. See ya!")


class Day:
	"""
	One day's worth of macro tracking. Stores all the macros for that day.
	has: a DATE; a list of food items/meals, FOOD; and two int trackers for CALORIES and PROTEIN
	can: add_food to its FOOD list; remove_food from its FOOD list
	"""

	def __init__(self, date):
		self.date = date
		self.food = []
		self.calories = 0
		self.protein = 0

	def add_food(self, name, cal, pro):
		self.food.append(Food(name, cal, pro))
		self.calories += int(cal)
		self.protein += int(pro)


	def remove_food(self, index):
		self.calories -= self.food[index].calories
		self.protein -= self.food[index].protein
		self.food.pop(index)


class Food:
	"""
	one food item or meal
	has: a NAME; number of CALORIES, number of PROTEIN
	"""

	def __init__(self, name, calories, protein):
		self.name = name
		self.calories = calories
		self.protein = protein

	def __str__(self):
		return '{0}: {1} Calories, {2}g Protein'.format(self.name, self.calories, self.protein)


def clear_screen():
	"""
	clears the command line screen
	"""
	os.system('cls')


def wait_sec(s):
	"""
	pauses command line for S seconds
	"""
	time.sleep(s)


MacTrac()


# def load_macros():
# 	days = {}
# 	try:
# 		file = open("MacFile.txt", "r")
# 	except FileNotFoundError:
# 		return days
# 	lines = deque(file.readlines())
# 	while lines:
# 		# get day info, make Day
# 		day_info = lines.popleft().split()
# 		day_year = int(day_info[0])
# 		day_month = int(day_info[1])
# 		day_day = int(day_info[2])
# 		day_items = int(day_info[3])
# 		day = Day(datetime.date(day_year, day_month, day_day))

# 		for _ in range(day_items):
# 			food_info = lines.popleft().split()
# 			food_name = food_info[0]
# 			food_calories = int(food_info[1])
# 			food_protein = int(food_info[2])
# 			day.food.append(Food(food_name, food_calories, food_protein))
# 			day.calories += food_calories
# 			day.protein += food_protein

# 		days[day.date] = day
# 		lines.popleft() #empty line

# 	file.close()
# 	return days


# def save_macros(days):
# 	file = open("MacFile.txt", "w")
# 	for day in days.values():
# 		file.write(str(day.date.year) + ' ' + str(day.date.month) + ' ' + str(day.date.day) + ' ' + str(len(day.food)) + '\n')
# 		for item in day.food:
# 			file.write(item.name + ' ' + str(item.calories) + ' ' + str(item.protein) + '\n')
# 		file.write('\n')

# 	file.close()