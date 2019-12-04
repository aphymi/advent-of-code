from collections import defaultdict
from typing import Dict, List, Set, Tuple

from util.parse import *

parse_input = split_on(",")

WirePath = List[str]
WirePaths = List[WirePath]
Point = Tuple[int, int]

def trace_paths(path: WirePath) -> Set[Point]:
	"""
	Return a set of all points that the given wire path visits.
	"""
	
	points = set()
	
	pos = (0, 0)
	
	for run in path:
		direction = run[0]
		run_length = int(run[1:])
		
		for _ in range(run_length):
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
	
def get_combined_steps(
		wire_paths: WirePaths,
		intersections: Set[Point],
		) -> Dict[Point, int]:
	"""
	Return a dictionary mapping from intersection points to the sum of the
	lengths of each wire it takes to get to that point from the origin.
	"""
	
	comb_steps = defaultdict(int)
	
	for wire_path in wire_paths:
		pos = (0, 0)
		running_path_len = 0
		
		visited = set()
		
		for leg in wire_path:
			direction = leg[0]
			run_length = int(leg[1:])
			
			for _ in range(run_length):
				running_path_len += 1
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
					comb_steps[pos] += running_path_len
	
	return comb_steps

def part1(wire_paths: WirePaths) -> int:
	intersections = (
		trace_paths(wire_paths[0])
		.intersection(trace_paths(wire_paths[1]))
	)
	
	return min(
		abs(i[0]) + abs(i[1])
		for i in intersections
	)

def part2(wire_paths: WirePaths) -> int:
	intersections = (
		trace_paths(wire_paths[0])
		.intersection(trace_paths(wire_paths[1]))
	)
	
	return min(get_combined_steps(wire_paths, intersections).values())
