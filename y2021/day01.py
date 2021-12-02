import functools

from util.parse import *
from util.utils import sliding_window


parse_input = compose(get_ints, lambda x: [y[0] for y in x])

def part1(depths) -> int:
	increases = 0
	last = float("inf")

	for number in depths:
		if number > last:
			increases += 1

		last = number
	
	return increases

def part2(depths) -> int:
	increases = 0
	last_sum = float("inf")

	for depth_set in sliding_window(depths, 3):
		depth_sum = sum(depth_set)
		if depth_sum > last_sum:
			increases += 1
		
		last_sum = depth_sum
	
	return increases
