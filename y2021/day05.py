from collections import defaultdict
from typing import List

from util.parse import *


Coordinate = Tuple[int, int]
CoordinateRange = Tuple[Coordinate, Coordinate]
CoordinateRanges = List[CoordinateRange]
def parse_input(inp: List[str]) -> CoordinateRanges:
	inp = get_ints(inp)

	return [
		((line[0], line[1]), (line[2], line[3]))
		for line in inp
	]

def get_step_size(x: int, y: int) -> int:
	if x == y:
		return 0
	
	if x < y:
		return 1
	
	return -1

def get_points_between(p1: Coordinate, p2: Coordinate) -> List[Coordinate]:
	x_step = get_step_size(p1[0], p2[0])
	y_step = get_step_size(p1[1], p2[1])

	points_between = []
	next_point = p1
	while next_point != p2:
		points_between.append(next_point)

		next_point = (next_point[0] + x_step, next_point[1] + y_step)
	
	points_between.append(p2)

	return points_between

def get_intersections(ranges: CoordinateRanges) -> int:
	covered_points = defaultdict(lambda: 0)

	for p1, p2 in ranges:
		points_between = get_points_between(p1, p2)

		for covered_point in points_between:
			covered_points[covered_point] += 1
	
	return sum(
		1
		for covered_count in covered_points.values()
		if covered_count > 1
	)

def part1(ranges: CoordinateRanges) -> int:
	relevant_ranges = [
		(p1, p2)
		for p1, p2 in ranges
		if p1[0] == p2[0] or p1[1] == p2[1]
	]

	return get_intersections(relevant_ranges)

def part2(ranges: CoordinateRanges) -> int:
	return get_intersections(ranges)
