#!/usr/bin/python3

import argparse
from importlib import import_module
import os
import sys

from input_retrieval import retrieve_input, retrieve_test_input

def dname(day):
	return "day{:02d}".format(day)

def yname(year):
	return "y{}".format(year)

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(
		description=(
			"Run the solver for a given day of the Advent of Code challenge."
		)
	)
	parser.add_argument(
		"day",
		type=int,
		help="which day to solve the problem for"
	)
	parser.add_argument(
		"--test",
		"-t",
		dest="testing",
		action="store_const",
		const=True,
		default=False,
		help="use test input (from .test file) instead of real input"
	)
	parser.add_argument(
		"--part",
		"-p",
		dest="part",
		default=None,
		choices=("1", "2"),
		help="the particular part to solve; defaults to both"
	)
	
	known_years = [
		int(dirname[1:])
		for dirname in os.listdir(".")
		if dirname.startswith("y")
	]
	parser.add_argument(
		"--year",
		"-y",
		dest="year",
		default=max(known_years),
		type=int,
		choices=known_years,
		help="the particular year to solve for; defaults to latest"
	)
	
	args = parser.parse_args()
	
	if not 1 <= args.day <= 25:
		print("Error: Day must be in range [1,25].")
		sys.exit(1)
	
	try:
		solver_module = import_module(
			"y{year}.day{day:02d}".format(
				year=args.year,
				day=args.day,
			)
		)
	
	except ImportError:
		raise Exception(f"No solver found for year {args.year}, day {args.day}")
	
	if args.testing:
		solver_input = retrieve_test_input()
	
	else:
		solver_input = retrieve_input(args.year, args.day)
	
	parts_to_eval = ("1", "2") if args.part is None else (args.part,)

	# If the solver module has a specification for input formatting, run it.
	if hasattr(solver_module, "parse_input"):
		solver_input = solver_module.parse_input(solver_input)
	
	
	for part in parts_to_eval:
		part_name = "part" + part
		if not hasattr(solver_module, part_name):
			print(
				f"Error: Solution for year {args.year}, day {args.day} has no "
				f"function {part_name}."
			)
		else:
			part_solver = getattr(solver_module, part_name)
			part_solution = part_solver(solver_input)
			
			print(f"Part {part} solution: {part_solution}")
