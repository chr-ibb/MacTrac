"""
Learned:
how to use enumerate to for loop through a list and have the item in the list AND the index
how to use deque, a container that pops from the begining better than lists
opening, reading, writing files
dictionaries and for loops
"""


import datetime
import time
import os
from collections import deque


def MacTrac():
	clear_screen()
	print("MacTrac")
	print("Loading saved macros...")
	days = load_macros()
	print("Finished loading!")
	wait_sec(1)
	
	while True:
		clear_screen()
		choice = input("(A)dd Macro, (V)iew Macros, or (E)xit? (a/v/e): ")
		if choice == 'a' or choice == 'A':
			add_macro(days)
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

def add_macro(days):
	date = pick_day()
	if date not in days:
		days[date] = Day(date)
	days[date].add_food()


def view_macro(days):
	date = pick_day()
	clear_screen()
	if date in days:
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
	days = {}
	try:
		file = open("MacFile.txt", "r")
	except FileNotFoundError:
		return days
	lines = deque(file.readlines())
	while lines:
		# get day info, make Day
		day_info = lines.popleft().split()
		day_year = int(day_info[0])
		day_month = int(day_info[1])
		day_day = int(day_info[2])
		day_items = int(day_info[3])
		day = Day(datetime.date(day_year, day_month, day_day))

		for _ in range(day_items):
			food_info = lines.popleft().split()
			food_name = food_info[0]
			food_calories = int(food_info[1])
			food_protein = int(food_info[2])
			day.food.append(Food(food_name, food_calories, food_protein))
			day.calories += food_calories
			day.protein += food_protein

		days[day.date] = day
		lines.popleft() #empty line

	file.close()
	return days


def save_macros(days):
	file = open("MacFile.txt", "w")
	for day in days.values():
		file.write(str(day.date.year) + ' ' + str(day.date.month) + ' ' + str(day.date.day) + ' ' + str(len(day.food)) + '\n')
		for item in day.food:
			file.write(item.name + ' ' + str(item.calories) + ' ' + str(item.protein) + '\n')
		file.write('\n')

	file.close()


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