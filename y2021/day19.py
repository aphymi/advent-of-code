from collections import Counter, defaultdict, deque
import itertools
from pprint import pprint
import math
from typing import Generator, Optional

from util.parse import *
from util.utils import manhattan_distance


parse_input = compose(
	lambda lines: "\n".join(lines),
	lambda line: line.split("\n\n"),
	split_on("\n"),
	# Discard ---scanner x--- lines
	map_func(lambda scanner_data: scanner_data[1:]),
	map_func(
		map_func(
			lambda line: tuple(int(value) for value in line.split(",")),
		),
	),
)

Coords = tuple[int, int, int]
CoordDistance = tuple[int, int, int]
ScannerData = list[Coords]

def get_distance_components(c1: Coords, c2: Coords) -> tuple[int, int, int]:
	return (
		c1[0] - c2[0],
		c1[1] - c2[1],
		c1[2] - c2[2],
	)

def add_distance_components(c: Coords, diff: tuple[int, int, int]) -> Coords:
	return (c[0] + diff[0], c[1] + diff[1], c[2] + diff[2])

def get_coordinate_rotations(c: Coords) -> Generator[Coords, None, None]:
	x, y, z = c

	face_rotations = [
		(x, y, z),
		(-y, x, z),
		(-x, -y, z),
		(y, -x, z),
		(x, -z, y),
		(x, z, -y),
	]

	for rx, ry, rz in face_rotations:
		turns = (
			(rx, ry, rz),
			(-rz, ry, rx),
			(rz, ry, -rx),
			(-rx, ry, -rz),
		)

		for tx, ty, tz in turns:
			yield (tx, ty, tz)

def get_rotations_in_parallel(
	coordinate_list: list[Coords],
) -> Generator[list[Coords], None, None]:
	return zip(
		*([
			get_coordinate_rotations(c)
			for c in coordinate_list
		])
	)

def get_combined_scanner_data(
	known: ScannerData,
	new: ScannerData,
) -> Optional[tuple[ScannerData, tuple[int, int, int]]]:
	known_point_set = set(known)

	# This is a pretty ugly brute-force solution, but! It still runs in under
	# a minute, so I'm not *too* ashamed.
	for new_rotation in get_rotations_in_parallel(new):
		# Compare every pair of points in known and new, to see if they match
		for known_point in known:
			for new_point in new_rotation:
				# If twelve or more points are displaced by this exact diff,
				# then we've found a correct correspondence. known_point is the
				# same beacon as new_point.
				diff = get_distance_components(known_point, new_point)
				shifted_new_set = set(
					add_distance_components(newer_point, diff)
					for newer_point in new_rotation
				)

				if len(known_point_set.intersection(shifted_new_set)) >= 12:
					# Return new list of scanner data, and discovered position
					# of new scanner
					return (
						known_point_set.union(shifted_new_set),
						diff,
					)
	
	return None

def combine_scanner_datas(
	scanner_datas: list[ScannerData],
) -> tuple[ScannerData, list[tuple[int, int, int]]]:
	queue = deque(scanner_datas)

	# Start with a basis of the first set of scanner data
	known_data = queue.popleft()
	scanner_positions = []
	
	while len(queue) > 0:
		new_data = queue.popleft()

		maybe_combined_data = get_combined_scanner_data(known_data, new_data)

		if maybe_combined_data is None:
			# We failed to combine them; pop it onto the end of the queue and
			# try again with more data later
			queue.append(new_data)
		
		else:
			# We succeeded combining them! Roll it into the known data
			combined_data, scanner_pos = maybe_combined_data
			known_data = combined_data
			scanner_positions.append(scanner_pos)
	

	return (known_data, scanner_positions)

full_data_and_scanners = None

def part1(data: list[ScannerData]) -> int:
	global full_data_and_scanners
	full_data_and_scanners = (
		full_data_and_scanners or combine_scanner_datas(data)
	)
	full_data, _scanner_positions = full_data_and_scanners

	return len(full_data)

def part2(data: list[ScannerData]) -> int:
	global full_data_and_scanners
	full_data_and_scanners = (
		full_data_and_scanners or combine_scanner_datas(data)
	)
	_full_data, scanner_positions = full_data_and_scanners

	aa, bb = max(
		itertools.combinations(scanner_positions, 2),
		key=lambda t: manhattan_distance(t[0], t[1]),
	)

	print(aa, bb)
	return manhattan_distance(aa, bb)
