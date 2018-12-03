#!/usr/bin/python3

import argparse
from importlib import import_module
import sys

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
		with open("inputs/" + day_name + ".txt") as file:
			split_input = file.read().split("\n")
	
	except FileNotFoundError:
		print("Error: No input file found for {}.".format(day_name))
		sys.exit(1)
	
	try:
		day_mod = import_module("sols." + day_name)
	
	except ImportError:
		print("Error: No solution module found for {}.".format(day_name))
		sys.exit(1)
	
	parts_to_eval = ("1", "2") if args.part is None else (args.part,)
	
	for part in parts_to_eval:
		part_name = "part" + part
		if not hasattr(day_mod, part_name):
			print("Error: Solution for day {} has no function {}.".format(args.day, part_name))
		else:
			print("Part {} answer: {}".format(part, getattr(day_mod, part_name)(split_input)))
