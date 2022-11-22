#!/usr/bin/python3

import argparse
from importlib import import_module
import inspect
import os
import pathlib
import sys
import time
import types

from input_retrieval import retrieve_input, retrieve_test_input

def dname(day):
	return "day{:02d}".format(day)

def yname(year):
	return "y{}".format(year)

def initialise_solver(year: int, day: int) -> None:
	year_dir = f"y{year}"
	day_file_path = f"{year_dir}/day{day:02d}.py"
	input_dir = f"{year_dir}/inputs"
	input_file_path = f"{input_dir}/day{day:02d}.txt"

	pathlib.Path(input_dir).mkdir(parents=True, exist_ok=True)

	if not os.path.exists(day_file_path):
		# use cleandoc to remove leading indentation
		initial_solver_code = (
			inspect.cleandoc(
				"""
				from util.parse import *


				parse_input = get_ints

				def part1(inp) -> int:
					return 0
				
				def part2(inp) -> int:
					return 0
				"""
			).replace(" " * 8, "\t")
			+ "\n"
		)

		with open(day_file_path, "w") as day_file:
			day_file.write(initial_solver_code)
		
		print(f"No solver found; initialising at {day_file_path}")
	
	if not os.path.exists(input_file_path):
		retrieve_input(year, day)


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
		"--init",
		"-i",
		dest="init",
		action="store_const",
		const=True,
		default=False,
		help=(
			"instead of running the day solver, initialise the given day's "
			"solver script and input"
		)
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
	
	if args.init:
		initialise_solver(args.year, args.day)
		sys.exit(0)
	
	solver_module: types.ModuleType
	try:
		solver_module = import_module(
			"y{year}.day{day:02d}".format(
				year=args.year,
				day=args.day,
			)
		)
	
	except ImportError:
		print(f"No solver found for year {args.year}, day {args.day}")
		sys.exit(1)
		
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
			start = time.time()
			part_solution = part_solver(solver_input)
			end = time.time()

			total_time = round(end - start, 2)
			
			print(f"Part {part} solution ({total_time}s): {part_solution}")
