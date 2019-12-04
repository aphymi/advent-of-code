from collections import deque
import math
from typing import List

from util.parse import *

parse_input = map_func(int)

def get_req_fuel(mass: int) -> int:
	return math.floor(mass/3) - 2

def part1(masses: List[int]) -> int: # 4.5m
	return sum(
		get_req_fuel(mass)
		for mass in masses
	)

def part2(masses: List[int]) -> int: #10m + 50s
	total_fuel = 0
	
	calc_q = deque(masses)
	
	while len(calc_q) > 0:
		new_mass = calc_q.popleft()
		
		req_fuel = get_req_fuel(new_mass)
		
		if req_fuel <= 0:
			continue
		
		total_fuel += req_fuel
		calc_q.appendleft(req_fuel)
	
	return total_fuel
