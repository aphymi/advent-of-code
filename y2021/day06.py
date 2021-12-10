import collections

from util.parse import *


parse_input = compose(get_ints, single_line)

def simulate_fish(ages: list[int], days: int) -> int:
	fishes = collections.defaultdict(int, collections.Counter(ages))

	for _i in range(days):
		ready_to_breed_count = fishes[0]

		for possible_age in range(1, 10):
			# right limit is one more than max age, to reset max age
			fishes[possible_age - 1] = fishes[possible_age]
		
		fishes[6] += ready_to_breed_count
		fishes[8] += ready_to_breed_count

	return sum(fishes.values())

def part1(ages: list[int]) -> int:
	return simulate_fish(ages, 80)

def part2(ages: list[int]) -> int:
	return simulate_fish(ages, 256)
