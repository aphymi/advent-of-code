from typing import Optional

from util.parse import *
from util.printing import print_over_current


parse_input = single_line

RockMap = list[list[str]]
Rock = list[list[str]]
Coords = tuple[int, int]

rocks: list[Rock] = [
	[list(rock_line) for rock_line in rock]
	for rock in [
		[
			"####",
		],
		[
			".#.",
			"###",
			".#.",
		],
		[
			"..#",
			"..#",
			"###",
		],
		[
			"#",
			"#",
			"#",
			"#",
		],
		[
			"##",
			"##",
		],
	]
]

def clamp_rock_map(
	rock_map: RockMap,
	how_far_down_to_check_for_floor: int,
) -> tuple[RockMap, int]:
	"""
	Reduce the height of the rock map as much as possible.

	First, remove as much empty height from the top of the map as possible.

	Then, look as far down in the map as specified to try to find a completely
	full row, at which point the map can be cut off there.
	
	Return the (possibly changed) rock map, and the number of row cut off in the
	last step.
	"""

	map_width = len(rock_map[0])
	empty_row = ["."] * map_width

	b = len(rock_map)
	while rock_map[-1] == empty_row:
		rock_map.pop()

	d = False
	if len(rock_map) == 381:
		d = True
	
	full_row = ["#"] * map_width
	rows_cut_off = 0
	for y in range(len(rock_map) - 1, how_far_down_to_check_for_floor - 1, -1):
		if rock_map[y] == full_row:
			rows_cut_off = y + 1
			rock_map = rock_map[y+1:]
			break

	return (rock_map, rows_cut_off)


def add_rock_map_height(
	rock_map: RockMap,
	height_to_add: int,
	map_width: Optional[int] = None,
) -> None:
	if map_width is None:
		map_width = len(rock_map[0])

	for _i in range(height_to_add):
		rock_map.append(["."] * map_width)

def rock_can_occupy(
	rock_map: RockMap,
	rock: Rock,
	rock_coords: Coords,
) -> bool:
	x, y = rock_coords
	rock_height = len(rock)
	rock_width = len(rock[0])

	map_width = len(rock_map[0])
	
	if x < 0:
		return False

	if y - (rock_height - 1) < 0:
		return False
	
	if x + (rock_width - 1) > (map_width - 1):
		return False
	
	map_area_to_occupy = [
		rock_line[x:x+rock_width]
		for rock_line in reversed(rock_map[y-rock_height+1:y+1])
	]

	return all(
		all(
			not (rock_char == "#" and map_char == "#")
			for rock_char, map_char in zip(rock_row, map_row)
		)
		for rock_row, map_row in zip(rock, map_area_to_occupy)
	)

def step_rock(
	rock_map: RockMap,
	rock: Rock,
	rock_coords: Coords,
	wind_direction: str,
) -> Optional[Coords]:
	"""
	Attempt to simulate a rock movement step.

	If the rock finds its resting place, rock_map will be modified accordingly
	and the function will return None.

	Otherwise, the rock's new coordinates will be returned.
	"""
	
	rock_x, rock_y = rock_coords
	x_modifier = -1 if wind_direction == "<" else 1

	if rock_can_occupy(rock_map, rock, (rock_x + x_modifier, rock_y)):
		rock_x += x_modifier
	
	if not rock_can_occupy(rock_map, rock, (rock_x, rock_y - 1)):
		for rock_row_index, rock_row in enumerate(rock):
			for rock_col_index, rock_char in enumerate(rock_row):
				if rock_char == ".":
					continue

				rock_map[rock_y - rock_row_index][rock_x + rock_col_index] = (
					rock_char
				)
		
		return None
	
	return (rock_x, rock_y - 1)

def simulate_rocks(
	wind_instructions: str,
	rock_count: int,
) -> int:
	rock_map = []

	step_count = 0
	fallen_rock_count = 0
	abbreviated_tower_height = 0
	memo = {}
	while True:
		rock = rocks[fallen_rock_count % len(rocks)]
		fallen_rock_count += 1

		rock_height = len(rock)
		add_rock_map_height(rock_map, 3 + rock_height, 7)

		rock_coords = (2, len(rock_map) - 1)
		last_rock_coords = rock_coords

		while True:
			rock_coords = step_rock(
				rock_map,
				rock,
				rock_coords,
				wind_instructions[step_count % len(wind_instructions)],
			)
			step_count += 1

			if rock_coords is None:
				# the rock has settled
				break

			last_rock_coords = rock_coords
		
		rock_map, abbreviated_height = clamp_rock_map(
			rock_map,
			(last_rock_coords[1] - len(rock)),
		)

		abbreviated_tower_height += abbreviated_height

		cur_tower_height = abbreviated_tower_height + len(rock_map)

		key = (
			# the [-30:] at the end here is a heuristic necessary for the test
			# input, but not the real input.
			hash("".join("".join(row) for row in rock_map[-30:])),
			fallen_rock_count % len(rocks),
			step_count % len(wind_instructions),
		)
		if key in memo:
			# found a loop!
			former_fallen_rock_count, former_tower_height = memo[key]
			loop_length = fallen_rock_count - former_fallen_rock_count
			loop_height_difference = cur_tower_height - former_tower_height

			loops_left, rocks_after_loops = (
				divmod(rock_count - fallen_rock_count, loop_length)
			)
			
			abbreviated_tower_height += loop_height_difference * loops_left
			fallen_rock_count = rock_count - rocks_after_loops
			memo = {}
			continue

		memo[key] = (
			fallen_rock_count,
			cur_tower_height,
		)

		if fallen_rock_count >= rock_count:
			break
	
	return len(rock_map) + abbreviated_tower_height
		

def part1(wind_instructions: str) -> int:
	return simulate_rocks(wind_instructions, 2022)

def part2(wind_instructions: str) -> int:
	return simulate_rocks(wind_instructions, 10**12)
