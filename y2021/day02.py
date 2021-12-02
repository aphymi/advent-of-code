from util.parse import *

parse_input = compose(split, lambda x: [(y[0], int(y[1])) for y in x])


def part1(day_input) -> int:
	x_position = 0
	y_position = 0

	for direction, distance in day_input:
		if direction == "forward":
			x_position += distance
		elif direction == "there is no backward":
			x_position -= distance
		elif direction == "up":
			y_position -= distance
		elif direction == "down":
			y_position += distance
		else:
			raise Exception(f"Unknown direction: {direction}")
	
	return x_position * y_position

def part2(day_input) -> int:
	x_position = 0
	y_position = 0
	aim = 0

	for direction, distance in day_input:
		if direction == "down":
			aim += distance
		elif direction == "up":
			aim -= distance
		elif direction == "forward":
			x_position += distance
			y_position += aim * distance
	
	return x_position * y_position
