from typing import Tuple

from util.parse import *

parse_input = compose(get_pos_ints, single_line, tuple)

Range = Tuple[int, int]

def monotonically_increases(num: str) -> bool:
	last_digit = num[0]
	for next_digit in num[1:]:
		if last_digit > next_digit:
			return False
		last_digit = next_digit
	
	return True

def has_adjacent_digits(num: str) -> bool:
	last_digit = num[0]
	for next_digit in num[1:]:
		if last_digit == next_digit:
			return True
		last_digit = next_digit
	
	return False

def has_dual_adjacent_digits(num: str) -> bool:
	last_len = len(num)
	
	while num != "":
		num = num.lstrip(num[0])
		if len(num) == (last_len - 2):
			return True
		
		last_len = len(num)
	
	return False

def part1(solution_range: Range) -> int:
	# Make a lazy iterable parallel to the range of passwords, with a 1 if the
	# 	corresponding pw conforms to both conditions, or a 0 otherwise. Then,
	# 	sum up all the 1s to get the number of valid passwords.
	# This is a bit indirect, but it's lazy, so it avoids loading all the valid
	# 	passwords into memory.
	num_valid_passwords = sum(
		1 if monotonically_increases(pw) and has_adjacent_digits(pw) else 0
		for pw in map(str, range(solution_range[0], solution_range[1]+1))
	)
	
	return num_valid_passwords
	
def part2(solution_range: Range) -> int:
	num_valid_passwords = sum(
		1 if monotonically_increases(pw) and has_dual_adjacent_digits(pw) else 0
		for pw in map(str, range(solution_range[0], solution_range[1]+1))
	)
	
	return num_valid_passwords
