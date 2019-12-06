from itertools import permutations

from util.parse import *

def bidirect(lines):
	dists = {(line[0], line[2]): int(line[4]) for line in lines}
	dists.update({(line[2], line[0]): int(line[4]) for line in lines})
	return dists

parse_input = compose(split, bidirect)

def part1(dists):
	def shortest_route_from(rts, start): # Greedy!
		s = 0
		while rts:
			min_route = min((ls for ls in rts if ls[0] == start), key=lambda ls: rts[ls])
			s += rts[min_route]
			rts = {ls: d for ls, d in rts.items() if start not in ls}
			start = min_route[1]
		
		return s
	
	return min(shortest_route_from(dists, loc) for loc in set(l1 for l1, l2 in dists))

def part2(dists):
	def route_len(dists, route):
		return sum(dists[path] for path in zip(route[:-1], route[1:]))
	
	return max(route_len(dists, route) for route in permutations(set(l1 for l1, l2 in dists)))
