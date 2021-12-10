import functools
import math
import statistics

from util.parse import *


parse_input = compose(get_ints, single_line)

def part1(crab_positions: list[int]) -> int:
	alignment_point = int(statistics.median(crab_positions))

	return sum(
		abs(position - alignment_point)
		for position in crab_positions
	)

@functools.lru_cache(None)
def get_fuel_use_over(distance: int) -> int:
	return sum(range(1, distance + 1))

def get_fuel_use_toward(positions: list[int], alignment_point: int) -> int:
	return sum(
		get_fuel_use_over(abs(position - alignment_point))
		for position in positions
	)

def part2(crab_positions: list[int]) -> int:
	alignment_point = statistics.mean(crab_positions)

	return min(
		get_fuel_use_toward(crab_positions, math.floor(alignment_point)),
		get_fuel_use_toward(crab_positions, math.ceil(alignment_point)),
	)
