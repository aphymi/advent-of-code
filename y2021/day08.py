from typing import Callable

from util.parse import *


segments = frozenset[str]

display_example = tuple[list[segments], list[segments]]

display_examples = list[display_example]

def parse_input(lines: list[segments]) -> display_examples:
	displays = []
	for line in lines:
		all_digits, display_digits = [
			[
				frozenset(segs)
				for segs in trimmed_part.split(" ")
			]
			for trimmed_part in (
				part.strip()
				for part in line.split("|")
			)
		]

		displays.append((all_digits, display_digits))
	
	return displays

def part1(inp: display_examples) -> int:
	return sum(
		sum(
			1
			for digit in displayed_digits
			if len(digit) in (2, 4, 3, 7)
		)
		for _all_digits, displayed_digits in inp
	)

def solve_digits(all_digits: list[segments]) -> dict[int, segments]:
	digits = {}

	def get_digit(condition: Callable[[segments], bool]) -> segments:
		valid = [
			d for d in all_digits
			if condition(d)
		]
		if len(valid) > 1:
			print(valid)
		return valid[0]

	digits[1] = get_digit(lambda d: len(d) == 2)
	digits[4] = get_digit(lambda d: len(d) == 4)
	digits[7] = get_digit(lambda d: len(d) == 3)
	digits[8] = get_digit(lambda d: len(d) == 7)

	digits[3] = get_digit(lambda d: (
		len(d) == 5
		and len(d.intersection(digits[7]))
		and d.issuperset(digits[7])
	))

	digits[9] = get_digit(lambda d: (
		len(d) == 6
		and d.issuperset(digits[3])
	))

	digits[5] = get_digit(lambda d: (
		len(d) == 5
		and d.issubset(digits[9])
		and d != digits[3]
	))

	digits[6] = get_digit(lambda d: (
		d not in digits.values()
		and d.issuperset(digits[5])
	))

	digits[2] = get_digit(lambda d: (
		len(d) == 5
		and d not in digits.values()
	))

	digits[0] = get_digit(lambda d: d not in digits.values())

	return {value: key for key, value in digits.items()}

def get_displayed_number(
	all_digits: list[str],
	display_digits: list[str],
) -> int:
	digit_map = solve_digits(all_digits)
	
	return int(
		"".join(
			str(digit_map[digit])
			for digit in display_digits
		)
	)

def part2(inp: display_examples) -> int:
	return sum(
		get_displayed_number(all_digits, displayed_digits)
		for all_digits, displayed_digits in inp
	)
