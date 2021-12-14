from util.parse import *


Dots = set[tuple[int, int]]
Instructions = list[tuple[str, int]]
DotsAndInstructions = tuple[Dots, Instructions]

def parse_input(lines: list[str]) -> DotsAndInstructions:
	dot_lines, instruction_lines = [
		part.split("\n")
		for part in "\n".join(lines).split("\n\n")
	]

	dots = set(
		tuple(coords)
		for coords in get_ints(dot_lines)
	)

	instructions = [
		(regex_match[0][0], int(regex_match[0][1]))
		for regex_match in get_regex_matches("([xy])=(\d+)")(instruction_lines)
	]

	return (dots, instructions)

def fold_dots(dots: Dots, instruction: tuple[str, int]) -> Dots:
	new_dots = set()

	fold_axis, fold_line = instruction
	fold_index = 0 if fold_axis == "x" else 1

	for dot in dots:
		if dot[fold_index] > fold_line:
			editable_dot = list(dot)
			editable_dot[fold_index] = fold_line - (dot[fold_index] - fold_line)
			new_dots.add(tuple(editable_dot))

		else:
			new_dots.add(dot)
	
	return new_dots

def print_dots(dots: Dots) -> None:
	x_bound = max(dot[0] for dot in dots)
	y_bound = max(dot[1] for dot in dots)

	map = [
		[" " for _i in range(x_bound + 1)]
		for _j in range(y_bound + 1)
	]

	for x, y in dots:
		map[y][x] = "#"
	
	for row in map:
		for cell in row:
			print(cell, end="")
		print()

def part1(dots_and_instructions: DotsAndInstructions) -> int:
	new_dots = fold_dots(dots_and_instructions[0], dots_and_instructions[1][0])
	return len(new_dots)

def part2(dots_and_instructions: DotsAndInstructions) -> int:
	dots, instructions = dots_and_instructions

	for instruction in instructions:
		dots = fold_dots(dots, instruction)
	
	print_dots(dots)
	return 0
