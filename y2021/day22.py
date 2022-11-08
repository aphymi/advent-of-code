import functools
import math
import re
import time
from typing import Generator, Iterable, List, Tuple

from util.parse import *
from util.utils import pairwise


parse_input = compose(
	split_on(" "),
	parallel_tuple(
		lambda x: x == "on",
		lambda x: [int(y) for y in re.findall(r"-?\d+", x)],
	),
	# lambda x: print(x, end="\n\n\n") or x,
	parallel_tuple(
		lambda x: x,
		lambda xs: ((xs[0], xs[1] + 1), (xs[2], xs[3] + 1), (xs[4], xs[5] + 1)),
	),
)

Point = Tuple[int, int, int]
DimensionLimit = Tuple[int, int]
Cuboid = Tuple[DimensionLimit, DimensionLimit, DimensionLimit]
RebootStep = Tuple[bool, Cuboid]

def prod(nums: Iterable[float]) -> float:
	return functools.reduce(
		(lambda a, b: a * b),
		nums,
		1
	)

def get_dimension_splits(cuboids: List[Cuboid], dimension: int) -> List[int]:
	splits = set()
	for cuboid in cuboids:
		start, end = cuboid[dimension]
		splits.add(start)
		splits.add(end)
	
	return sorted(splits)

def get_non_overlapping_cuboids(
	cuboids: List[Cuboid],
) -> Generator[Cuboid, None, None]:
	x_splits, y_splits, z_splits = tuple(
		get_dimension_splits(cuboids, i)
		for i in range(3)
	)

	print("Starting...", end="\r")

	x_split_count = 0
	total_x_split_counts = len(x_splits) - 1

	for x_start, x_end in pairwise(x_splits):
		x_split_count += 1
		print("                        ", end="\r")
		print(f"({x_split_count}/{total_x_split_counts})", end="\r")
		for y_start, y_end in pairwise(y_splits):
			for z_start, z_end in pairwise(z_splits):
				yield (
					(x_start, x_end),
					(y_start, y_end),
					(z_start, z_end),
				)

def point_in_cuboid(point: Point, cuboid: Cuboid) -> bool:
	return all(
		cuboid[dimension][0] <= point[dimension] < cuboid[dimension][1]
		for dimension in range(3)
	)

def get_point_state(point: Point, reboot_steps: List[RebootStep]) -> bool:
	for state, reboot_cuboid in reboot_steps[::-1]:
		if point_in_cuboid(point, reboot_cuboid):
			return state
	
	return False

def get_cuboid_volume(cuboid: Cuboid) -> int:
	return prod(
		end - start
		for start, end in cuboid
	)

def get_cuboid_center(cuboid: Cuboid) -> Point:
	return tuple(
		(start + end) / 2
		for start, end in cuboid
	)

def get_activated_cubes(reboot_steps: List[RebootStep]) -> int:
	relevant_reboot_cuboids = get_non_overlapping_cuboids([
		cuboid
		for _state, cuboid in reboot_steps
	])

	activated_cubes = 0
	for relevant_reboot_cuboid in relevant_reboot_cuboids:
		center_point = get_cuboid_center(relevant_reboot_cuboid)

		if get_point_state(center_point, reboot_steps):
			activated_cubes += get_cuboid_volume(relevant_reboot_cuboid)
	
	return activated_cubes

def part1(full_reboot_steps: List[RebootStep]) -> int:
	initial_reboot_steps = [
		reboot_step
		for reboot_step in full_reboot_steps
		if all(
			abs(start) <= 50 and abs(end) <= 51
			for start, end in reboot_step[1]
		)
	]

	return get_activated_cubes(initial_reboot_steps)

def part2(full_reboot_steps: List[RebootStep]) -> int:
	start = time.time()
	value = get_activated_cubes(full_reboot_steps)
	end = time.time()
	print(f"{end - start}s")
	return value
