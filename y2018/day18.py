from util.gol import GameOfLife
from util.parse import *
parse_input = map_func(list)


class LumberYard(GameOfLife):
	def new_value(self, x, y, cur):
		adj = self.adj8(x, y)
		
		if cur == ".":
			return "|" if adj.count("|") >= 3 else "."
		
		elif cur == "|":
			return "#" if adj.count("#") >= 3 else "|"
		
		else: # cur == "#"
			return "#" if "|" in adj and "#" in adj else "."
	
	def score(self):
		return sum(row.count("|") for row in self.state) * sum(row.count("#") for row in self.state)
	
	def visualise(self):
		return "\n".join(" ".join(row) for row in self.state)

def part1(cur_map):
	yard = LumberYard(cur_map)
	yard.stepN(10)
	
	return yard.score()

def part2(cur_map):
	yard = LumberYard(cur_map)
	
	seen = set()
	cycle = []
	# Look for a state we see twice in a row.
	while True:
		yard.step()
		
		if cycle:
			if yard.state == cycle[0]: # Gotten back to the start of the cycle.
				break
			cycle.append(yard.state)
			
		else:
			tup = tuple(tuple(row) for row in yard.state)
			
			if tup in seen:
				cycle.append(yard.state)
				
			else:
				seen.add(tup)

	yard.state = cycle[(1000000000 - yard.t) % len(cycle)]
	return yard.score()

