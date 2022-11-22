import functools
import itertools
import math
from typing import Iterable

from util.parse import *
from util.printing import print_over_current


parse_input = compose(single_line, int)

@functools.cache
def get_divisors(n: int, max_factor: float = float("inf")) -> Iterable[int]:
	if n == 1:
		return [1]

	if n == 2:
		return [1, 2]

	divisors = set([1, n])
	for i in range(2, math.floor(math.sqrt(n)) + 2):
		if n % i == 0:
			divisors.add(i)
			divisors.add(n / i)
	
	return [
		divisor for divisor in divisors
		if divisor * max_factor >= n
	]

def calculate_presents(divisors: list[int], multiplier: int = 10) -> int:
	return sum(divisors) * multiplier

def part1(target_presents: int) -> int:
	for house_num in itertools.count(1):
		print_over_current(house_num)
		divisors = get_divisors(house_num)
		presents = calculate_presents(divisors)
		if presents >= target_presents:
			return house_num
		
def part2(target_presents: int) -> int:
	for house_num in itertools.count(1):
		print_over_current(house_num)
		divisors = get_divisors(house_num, 50)
		presents = calculate_presents(divisors, 11)
		if presents >= target_presents:
			return house_num
