import collections
import math
from typing import Generator

from util import tile_map

from util.parse import *


CaveMap = tile_map.TileMap[int]

def parse_input(lines: list[str]) -> CaveMap:
	return tile_map.TileMap([
		[
			int(char)
			for char in list(row)
		]
		for row in lines
	])

def get_low_points(
	map: tile_map.TileMap,
) -> Generator[tile_map.TileData, None, None]:
	for value, x, y in map.walk():
		is_low_point = all(
			adj_value > value
			for adj_value, _adj_x, _adj_y in map.get_adjacent_4(x, y)
		)
		if is_low_point:
			yield (value, x, y)

def part1(map: CaveMap) -> int:
	risk_sum = 0

	for height, _x, _y in get_low_points(map):
		risk_sum += 1 + height

	return risk_sum

def get_basin(
	map: CaveMap,
	low_point: tile_map.TileData
) -> list[tile_map.TileData]:
	known_basin = set()
	to_investigate = collections.deque([low_point])

	while len(to_investigate) > 0:
		height, x, y = to_investigate.popleft()

		if (x, y) in known_basin or height >= 9:
			continue
		
		known_basin.add((x, y))
		
		for adjacent in map.get_adjacent_4(x, y):
			to_investigate.append(adjacent)
	
	return known_basin

def part2(map: CaveMap) -> int:
	basins = []

	for low_point in get_low_points(map):
		basins.append(get_basin(map, low_point))
	
	basins.sort(key=lambda basin: -len(basin))

	largest_basins = basins[:3]

	return math.prod(len(basin) for basin in largest_basins)
