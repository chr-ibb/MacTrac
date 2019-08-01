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

-how to sort lists, and how to use a sorted list in conjunction with a dictionary

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
	I guess python sort of says to just try it and see if it's actually too slow..
	nah because I'm literally gonna have to check every single item each time i move to a new day
	ima use an ordered dict
	scatch that. I'll use a regular dictionary like I already am, but then I'll have an additional list of just the
	dates, which can be sorted. sick. 

todo:
	make a __repr__ and __str__ for Food items, so you can just straight up print them
	redo the remove method, make it just reprint the day but with the element number next to each item
	get rid of the ordreded list if you dont need it. right now you aren't using it
"""


import datetime
import time
import os
import msvcrt
# from collections import deque
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
	days, days_list = load_macros()
	passed = time.clock() - now
	print("Finished loading! Loading took {0} seconds\n".format(passed))

	input("press enter ")


	view_day = datetime.date.today()
	while True: #main loop
		clear_screen()
		print(title)

		view_macro(days, view_day)

		print("\nAdd / Remove macro here: (E) / (R)    Previous / Following day: (A) / (D)    Select by date: (S)    Exit: (Q)")
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
			print("Saving macros...")
			save_macros(days)
			input("Finished. See ya! ")
			return
		else:
			print("Please enter the letters E, A, D, S, or Q")
			wait_sec(1)

def add_macro(days, date):
	clear_screen()
	print(title)
	view_macro(days, date)

	name = input("Name of food item or meal: ")
	cal = input("Calories: ")
	pro = input("protein(g): ")
	if date not in days:
		days[date] = Day(date)
	days[date].add_food(name, cal, pro)


def remove_macro(days, date):
	if date in days:
		days[date].remove_food()
	else:
		input("nothing to remove...")


def view_macro(days, date):
	if date == datetime.date.today():
		day_print = 'Today,     ' + str(date)
	elif date == datetime.date.today() - datetime.timedelta(1):
		day_print = 'Yesterday, ' + str(date)
	else:
		day_print = '           ' + str(date)
	print(day_print)

	if date in days:
		day = days[date]
		print("\nTotal:", day.calories, "calories, ", str(day.protein) + 'g', "protein\n")
		for item in day.food:
			print(item)
	else:
		print("\nTotal: 0 calories, 0g protein\n")



def pick_day():
	clear_screen()
	print(title)

	year = int(input("year: "))
	month = int(input("month: "))
	day = int(input("day: "))

	return datetime.date(year, month, day)



def load_macros():
	try:
		with open('MacFile.pickle', 'rb') as f:
			days = pickle.load(f)
		days_list = list(days.keys())
		days_list.sort()
		return days, days_list
	except FileNotFoundError:
		return {}, []


def save_macros(days):
	with open ('MacFile.pickle', 'wb') as f:
		pickle.dump(days, f)


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

	def add_food(self, name, cal, pro):
		self.food.append(Food(name, cal, pro))
		self.calories += int(cal)
		self.protein += int(pro)


	def remove_food(self):
		while True:
			clear_screen()
			for i, item in enumerate(self.food):
				print(i, item.name)
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