#!/usr/bin/python3

import argparse
from importlib import import_module
import sys

import requests

def retrieve_day_input(day, day_name):
	
	try:
		with open("inputs/" + day_name + ".txt") as file:
			input_file = file.read()
	
	except FileNotFoundError:
		print("No input file found; retrieving input remotely.")
		try:
			with open(".session") as file:
				sess = file.read().strip()

		except FileNotFoundError:
			print("Error: Neither saved input file nor .session cookie file could be found.")
			sys.exit(1)
		
		r = requests.get("https://adventofcode.com/2018/day/{}/input".format(day),
							cookies={"session": sess})

		if r.status_code != 200:
			print("Error: Unable to retrieve input file.")
			sys.exit(1)
		
		input_file = r.text

		with open("inputs/" + day_name + ".txt", "w") as file:
			file.write(input_file)

	return input_file.splitlines()

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description="Solve a day of the advent of code.")
	parser.add_argument("day", metavar="day", type=int,
						help="the number of the day to solve")
	parser.add_argument("--part", "-p", dest="part", default=None, choices=("1", "2"),
						help="the particular part to solve, instead of both")
	
	args = parser.parse_args()
	
	if not 1 <= args.day <= 25:
		print("Error: Day must be in range [1,25].")
		sys.exit(1)
	
	day_name = "day{:02d}".format(args.day)
	
	try:
		day_mod = import_module("sols." + day_name)
	
	except ImportError:
		print("Error: No solution module found for {}.".format(day_name))
		sys.exit(1)
	
	input_lines = retrieve_day_input(args.day, day_name)
	
	parts_to_eval = ("1", "2") if args.part is None else (args.part,)

	if hasattr(day_mod, "preprocess_input"):
		input_lines = day_mod.preprocess_input(input_lines)
	
	for part in parts_to_eval:
		part_name = "part" + part
		if not hasattr(day_mod, part_name):
			print("Error: Solution for day {} has no function {}.".format(args.day, part_name))
		else:
			print("Part {} answer: {}".format(part, getattr(day_mod, part_name)(input_lines)))
