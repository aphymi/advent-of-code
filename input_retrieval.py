import os.path
from typing import List

import requests


def get_input_file_name(year: int, day: int) -> str:
	"""
	Return the name on disk of the input file for the specified day and year.
	"""
	
	return "y{year}/inputs/day{day:02d}.txt".format(
		year=year,
		day=day,
	)

def download_input_from_server(year: int, day:int) -> str:
	"""
	Download the specified input file from the server, and save it to disk for
		next time.
	
	Returns: The full contents of the input file.
	"""
	
	input_file_name = get_input_file_name(year, day)
	
	# Get the saved session cookie.
	try:
		with open(".session") as file:
			session = file.read().strip()
	
	# If we can't find a saved session cookie, raise an exception.
	except FileNotFoundError as ex:
		print("Error: No saved input or .session cookie found.")
		raise ex
	
	r = requests.get(
		f"https://adventofcode.com/{year}/day/{day}/input",
		cookies={"session": session},
		headers={
			"User-Agent": (
				"github.com/aphymi/advent-of-code/ by same username at gmail"
			),
		},
	)
	
	# If the server responded with a bad status code, raise an exception.
	if r.status_code != 200:
		raise Exception(
			"AoC server responded with bad status code when attempting to "
			f"retrieve input file: {r.status_code}"
		)
		
	# Otherwise, we're all good.
	input_contents = r.text
	
	# Save the retrieved input for next time.
	with open(input_file_name, "w") as file:
		file.write(input_contents.strip())
	
	return input_contents

def retrieve_input(year: int, day: int) -> List[str]:
	"""
	Get the input file for the day and year's challenge.
	
	If the specified input file is saved on disk, read it from there. Otherwise,
		download it from the AoC site, and save it to the disk for later use.
	
	Args:
		year: The year of the puzzle to retrieve the input for.
		day: The day of the challenge to retrieve the input for.
	
	Returns: A list of the lines of the input file.
	"""
	
	input_file_name = get_input_file_name(year, day)
	input_file_dir = os.path.dirname(input_file_name)
	
	if not os.path.isdir(input_file_dir):
		os.makedirs(input_file_dir)
	
	# First, try reading from a saved file.
	try:
		with open(input_file_name) as file:
			input_contents = file.read()
	
	# If that doesn't work, download it from the AoC site.
	except FileNotFoundError:
		print("No input file found; retrieving input from AoC site.")
		
		input_contents = download_input_from_server(year, day)
	
	return input_contents.splitlines()

def retrieve_test_input() -> List[str]:
	"""
	Get the test input located in test_input.txt.
	
	Returns: A list of the lines of the test input.
	"""
	
	with open("test_input.txt") as file:
		return file.read().splitlines()
