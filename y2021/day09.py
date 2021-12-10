import collections
import math
from typing import Generator, Generic, TypeVar

from util.parse import *


T = TypeVar("T")
TileData = tuple[T, int, int]

class TileMap(Generic[T]):
	def __init__(self, state: list[list[T]]) -> None:
		self.state = state
	
	def get_at(self, x: int, y: int) -> T:
		return self.state[y][x]

	def walk(self) -> Generator[TileData, None, None]:
		for y, row in enumerate(self.state):
			for x, value in enumerate(row):
				yield (value, x, y)

	def get_adjacent_4(self, x: int, y: int) -> list[TileData]:
		modifiers = [
			(0, -1),
			(-1, 0),
			(1, 0),
			(0, 1),
		]

		adjacent = []
		for modifier in modifiers:
			adj_x = x + modifier[0]
			adj_y = y + modifier[1]
				
			if adj_y not in range(len(self.state)):
				continue

			if adj_x not in range(len(self.state[adj_y])):
				continue
		
			adjacent.append((self.state[adj_y][adj_x], adj_x, adj_y))
		
		return adjacent


CaveMap = TileMap[int]

def parse_input(lines: list[str]) -> CaveMap:
	return TileMap([
		[
			int(char)
			for char in list(row)
		]
		for row in lines
	])

def get_low_points(map: TileMap[T]) -> Generator[TileData, None, None]:
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

def get_basin(map: CaveMap, low_point: TileData) -> list[TileData]:
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
