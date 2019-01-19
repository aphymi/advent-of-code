from itertools import combinations, chain

from util.parse import *
parse_input = map_func(int)

def part1(containers):
	successes = 0
	for conts in chain(*(combinations(containers, r+1) for r in range(len(containers)))):
		if sum(conts) == 150:
			successes += 1
	
	return successes

def part2(containers):
	for r in range(1, len(containers)+1):
		good_combos = [conts for conts in combinations(containers, r) if sum(conts) == 150]
		if good_combos:
			return len(good_combos)
