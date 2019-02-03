#!/usr/bin/python3

import argparse
from importlib import import_module
import os
import sys

import requests

def dname(day):
	return "day{:02d}".format(day)

def yname(year):
	return "y{}".format(year)

def retrieve_input(year, day):
	file_dir = "{}/inputs/".format(yname(year))
	file_name = file_dir + "{}.txt".format(dname(day))
	if not os.path.isdir(file_dir):
		os.makedirs(file_dir)
	
	try:
		with open(file_name) as file:
			input_file = file.read()
	
	except FileNotFoundError:
		print("No input file found; retrieving input remotely.")
		try:
			with open(".session") as file:
				sess = file.read().strip()

		except FileNotFoundError:
			print("Error: Neither saved input file nor .session cookie file could be found.")
			sys.exit(1)
		
		r = requests.get("https://adventofcode.com/{}/day/{}/input".format(year, day),
							cookies={"session": sess})

		if r.status_code != 200:
			print("Error: Unable to retrieve input file.")
			sys.exit(1)
		
		input_file = r.text

		with open(file_name, "w") as file:
			file.write(input_file.strip())

	return input_file.splitlines()

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description="Solve a day of the advent of code.")
	parser.add_argument("day", type=int,
						help="which day to solve the problem for")
	parser.add_argument("-t", "--test", dest="testing",
						action="store_const", const=True, default=False,
						help="read input from the test file .test")
	parser.add_argument("--part", "-p", dest="part", default=None, choices=("1", "2"),
						help="the particular part to solve, instead of both")
	years = [dirname[1:] for dirname in os.listdir(".") if dirname.startswith("y")]
	parser.add_argument("--year", "-y", dest="year", default=max(years), choices=years,
						help="which year to solve the day for")
	
	args = parser.parse_args()
	
	if not 1 <= args.day <= 25:
		print("Error: Day must be in range [1,25].")
		sys.exit(1)
	
	try:
		day_mod = import_module("{}.{}".format(yname(args.year), dname(args.day)))
	
	except ImportError:
		print("Error: No solution module found for {}-{}.".format(yname(args.year), dname(args.day)))
		sys.exit(1)
	
	if args.testing:
		with open(".test") as file:
			lines = file.read().splitlines()
	
	else:
		lines = retrieve_input(args.year, args.day)
	
	parts_to_eval = ("1", "2") if args.part is None else (args.part,)

	if hasattr(day_mod, "parse_input"):
		lines = day_mod.parse_input(lines)
	
	for part in parts_to_eval:
		part_name = "part" + part
		if not hasattr(day_mod, part_name):
			print("Error: Solution for year-{} day-{} has no function {}.".format(args.year, args.day, part_name))
		else:
			print("Part {} answer: {}".format(part, getattr(day_mod, part_name)(lines)))
