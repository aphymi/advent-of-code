from typing import Optional

from util.parse import *
from util.printing import print_over_current


parse_input = compose(
	get_ints,
	map_func(
		lambda line: ((line[0], line[1]), (line[2], line[3])),
	),
)

Coord = tuple[int, int]
SensorBeaconPair = tuple[Coord, Coord]

def get_m_distance(c1: Coord, c2: Coord) -> int:
	return sum(abs(c1p - c2p) for c1p, c2p in zip(c1, c2))

def get_covered_range_at(
	sensor: Coord,
	covered_distance: int,
	y_level: int,
	x_bounds: tuple[int, int] = (float("-inf"), float("inf")),
) -> Optional[tuple[int, int]]:
	sensor_distance_from_y_level = abs(sensor[1] - y_level)
	if sensor_distance_from_y_level > covered_distance:
		return None

	covered_x_distance = covered_distance - sensor_distance_from_y_level

	left = max(
		sensor[0] - covered_x_distance,
		x_bounds[0],
	)
	right = min(
		sensor[0] + covered_x_distance,
		x_bounds[1],
	)

	if not sensor[0] in range(left, right + 1):
		return None

	return (
		left,
		right,
	)

def get_total_range_cover(
	ranges: list[tuple[int, int]],
) -> int:
	range_cover = 0
	last_range_end = None
	
	for start, end in sorted(ranges):
		if end < start:
			start, end = end, start

		if last_range_end is not None:
			if end <= last_range_end:
				continue

			if start <= last_range_end:
				start = last_range_end + 1
		
		range_cover += (end - start) + 1
		last_range_end = end
	
	return range_cover

def get_free_x(
	ranges: list[tuple[int, int]],
	bounds: tuple[int, int],
) -> Optional[int]:
	# assumes there is most a single uncovered space
	furthest_end = None

	for start, end in sorted(ranges):
		if furthest_end is None:
			if start > bounds[0]:
				return bounds[0]

			furthest_end = end
			continue
		
		if start > (furthest_end + 1):
			return start - 1
		
		if end > furthest_end:
			furthest_end = end
	
	if furthest_end < bounds[1]:
		return bounds[1]
	
	return None

def part1(sensor_beacon_pairs: list[SensorBeaconPair]) -> int:
	# 10 for test input, 2 million for real input
	relevant_level = 10 if len(sensor_beacon_pairs) <= 14 else 2 * 10**6

	ranges = []
	for sensor, beacon in sensor_beacon_pairs:
		covered_range = get_covered_range_at(
			sensor,
			get_m_distance(sensor, beacon),
			relevant_level,
		)

		if covered_range is not None:
			ranges.append(covered_range)
	
	covered_distance = get_total_range_cover(ranges)

	beacon_count = len(set(
		beacon
		for _sensor, beacon in sensor_beacon_pairs
		if beacon[1] == relevant_level
	))

	return covered_distance - beacon_count

def part2(sensor_beacon_pairs: list[SensorBeaconPair]) -> int:
	dimension_clamp = 20 if len(sensor_beacon_pairs) <= 14 else 4 * 10**6

	bounds = (0, dimension_clamp)

	sensor_reaches = {
		sensor: get_m_distance(sensor, beacon)
		for sensor, beacon in sensor_beacon_pairs
	}

	for y in range(bounds[0], bounds[1] + 1):
		ranges = []
		for sensor, _beacon in sensor_beacon_pairs:
			covered_range = get_covered_range_at(
				sensor,
				sensor_reaches[sensor],
				y,
				bounds,
			)

			if covered_range is not None:
				ranges.append(covered_range)
		
		ranges.sort()

		free_x = get_free_x(
			ranges,
			bounds,
		)

		if free_x is not None:
			return free_x * (4 * 10**6) + y

	raise Exception("Couldn't find free x")
