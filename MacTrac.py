"""
Learned:
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

TODO
make the ui look nicer
maybe move all the printing outside of the classes
maybe eventually use Clui for this
make it so you can view by week or month, to see how well you're doing over time
like show averages, or even graphs


NEW DESIGN IDEA:
you start up mactrac, 
it opens up and shows TODAY (so none if theres no entries yet)
you can either:
	use WASD to cycle through days,
	enter a new item onto the day that is showing currently
	or enter a day you want to see manually

It'll say "today" and the date if it's showing today
It'll say "yesterday" and the date if its showing yesterday
otherwise it just shows the date

to Solve:
	how to get the days in order.... as of now they are in an unordered dictionary...
	do I use orderedDict? do I just loop through until i find the next day in that direction? 
	do i just look through all the days until i find the previous one, and if i dont find it, then just look
	for the date previous that one? thats such a huge waste of time though...
"""


import datetime
import time
import os
from collections import deque
import pickle

title = ''
title += "  #   #               #######                \n"
title += " # # # #                 #                   \n"
title += " # # # #    ##    ###    #   # ###  ##    ###\n"
title += "#   #   #  #  #  #       #   ##    #  #  #   \n"
title += "#   #   #  #  #  #       #   #     #  #  #   \n"
title += "#   #   #   ## #  ###    #   #      ## #  ###\n"

def MacTrac():
	clear_screen()
	print(title)
	print("Loading saved macros...\n")
	now = time.clock()
	days = load_macros()
	passed = time.clock() - now
	print("Finished loading! Loading took {0} seconds\n".format(passed))
	input("press enter ")
	
	while True:
		clear_screen()
		print(title)
		choice = input("(A)dd Macro, (V)iew Macros, or (E)xit? (a/v/e): ")
		if choice == 'a' or choice == 'A':
			add_macro(days, pick_day())
		elif choice == 'v' or choice == 'V':
			view_macro(days)
		elif choice == 'e' or choice == 'E':
			print("Saving macros...")
			save_macros(days)
			input("Finished. See ya! ")
			return
		else:
			print("Please enter the letters (a) or (v) or (e)")
			wait_sec(1)

def add_macro(days, date):
	if date not in days:
		days[date] = Day(date)
	days[date].add_food()


def view_macro(days):
	clear_screen()
	print(title)
	if date in days:
		print('     ', date)
		day = days[date]
		for item in day.food:
			print(item.name + ':', item.calories, "calories,", str(item.protein) + 'g', "protein")
		print("\nTotal:", day.calories, "calories, ", str(day.protein) + 'g', "protein\n")
		input("Press Enter to return ")
	else:
		print("no macros saved for", date)
		input("press enter ")


def pick_day():
	today = datetime.date.today()
	while True:
		clear_screen()
		print(title)
		print("(T)oday, (Y)esterday, (O)ther")
		day = input("Which day? (t/y/o): ")
		if day == 't' or day == 'T':
			return today
		elif day == 'y' or day == 'Y':
			return today - datetime.timedelta(1)
		elif day == 'o' or day == 'O':
			year = int(input("year: "))
			month = int(input("month: "))
			day = int(input("day: "))
			return datetime.date(year, month, day)
		else:
			print("Something went wrong, try again.")


def load_macros():
	try:
		with open('MacFile.pickle', 'rb') as f:
			data = pickle.load(f)
		return data
	except FileNotFoundError:
		return{}


def save_macros(data):
	with open ('MacFile.pickle', 'wb') as f:
		pickle.dump(data, f)


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


class Day:
	"""
	One day's worth of macro tracking. stores all the macros for that day.
	has: a DATE; a list of food items/meals, FOOD; and two int trackers for CALORIES and PROTEIN
	"""

	def __init__(self, date):
		self.date = date
		self.food = []
		self.calories = 0
		self.protein = 0

	def add_food(self):
		while True:
			clear_screen()
			name = input("name of food item or meal: ")
			if ' ' in name:
				name = name.replace(' ', '_')

			cal = input("Calories: ")
			pro = input("protein(g): ")
			correct = input(name + ', ' + cal + ' calories, ' + pro + 'g protein? (y/n): ')
			if correct == 'y' or 'Y':
				self.food.append(Food(name, cal, pro))
				self.calories += int(cal)
				self.protein += int(pro)
				return

	def remove_food(self):
		while True:
			clear_screen()
			for i, item in enumerate(self.food):
				print(i, item)
			to_remove = input("Remove which? Enter number: ")
			assert type(to_remove) is int, "you must enter a number"
			correct = input("Remove " + item.name + ", " + item.calories + '/' + item.protein + "? (y/n): ")
			if correct == 'y' or 'Y':
				return self.food.pop(to_remove)


class Food:
	"""
	one food item or meal
	has: a NAME; number of CALORIES, number of PROTEIN
	"""

	def __init__(self, name, calories, protein):
		self.name = name
		self.calories = calories
		self.protein = protein


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