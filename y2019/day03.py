from collections import defaultdict
from typing import Dict, List, Set, Tuple

from util.parse import *

parse_input = split_on(",")

def trace_paths(paths) -> Set[Tuple[int, int]]:
	points = set()
	
	pos = (0, 0)
	
	for path in paths:
		direction = path[0]
		steps = int(path[1:])
		
		for _ in range(steps):
			if direction == "R":
				pos = (pos[0]+1, pos[1])
			elif direction == "L":
				pos = (pos[0]-1, pos[1])
			elif direction == "U":
				pos = (pos[0], pos[1]+1)
			else: # direction == "D"
				pos = (pos[0], pos[1]-1)
			
			points.add(pos)
	
	return points
	
def get_combined_steps(wire_paths, intersections) -> Dict[Tuple[int, int], int]:
	comb_steps = defaultdict(int)
	
	for wire_path in wire_paths:
		pos = (0, 0)
		path_steps = 0
		
		visited = set()
		
		for leg in wire_path:
			direction = leg[0]
			steps = int(leg[1:])
			
			for _ in range(steps):
				path_steps += 1
				if direction == "R":
					pos = (pos[0]+1, pos[1])
				elif direction == "L":
					pos = (pos[0]-1, pos[1])
				elif direction == "U":
					pos = (pos[0], pos[1]+1)
				else: # direction == "D"
					pos = (pos[0], pos[1]-1)
				
				if pos in intersections and pos not in visited:
					visited.add(pos)
					comb_steps[pos] += path_steps
	
	return comb_steps

def part1(wire_paths: List[List[str]]) -> int:
	intersections = (
		trace_paths(wire_paths[0])
		.intersection(trace_paths(wire_paths[1]))
	)
	
	return min(
		abs(i[0]) + abs(i[1])
		for i in intersections
	)

def part2(wire_paths) -> int:
	intersections = (
		trace_paths(wire_paths[0])
		.intersection(trace_paths(wire_paths[1]))
	)
	
	return min(get_combined_steps(wire_paths, intersections).values())
