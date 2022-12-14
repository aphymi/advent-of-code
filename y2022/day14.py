import copy
from typing import Generic, Optional, Union

from util.parse import *
from util.tile_map import TileMap
from util.utils import chunk, pairwise


parse_input = compose(
	get_ints,
	map_func(lambda line: list(chunk(line, 2))),
)

class LazyTileMap(Generic[T]):
	"""
	A two-dimensional grid of a generic type, without a hard boundary.

	Only tiles that are not empty are kept in memory.
	"""

	def __init__(
		self,
		initial_content: dict[tuple[int, int], T] = {},
		filler: T = None,
	) -> None:
		self.state = copy.deepcopy(initial_content)
		self.filler = filler
	
	def get_at(
		self,
		x: int,
		y: int,
		safe: bool = True,
	) -> T:
		"""
		Return the value at the given x and y coordinates.

		Returns the filler value if the coordinate is empty.
		"""

		if (x, y) in self.state:
			return self.state[(x, y)]
		
		return self.filler
	
	def set_at(self, x: int, y: int, new_value: T) -> None:
		"""
		Set the given value at the given x and y coordinates.
		
		Deletes the value from memory, if new_value is equal to the filler
		value.
		"""

		if new_value == self.filler:
			del self.state[(x, y)]
		
		else:
			self.state[(x, y)] = new_value
	
	def print(self) -> None:
		xs = set(coord[0] for coord in self.state.keys())
		ys = set(coord[1] for coord in self.state.keys())

		for y in range(min(ys), max(ys)):
			print("".join(
				self.get_at(x, y)
				for x in range(min(xs), max(xs) + 1)
			))

Coord = tuple[int, int]
RockPath = list[Coord]
CaveMap = Union[TileMap[str], LazyTileMap[str]]

def draw_map(rock_paths: list[list[tuple[int, int]]]) -> CaveMap:
	xs = [
		coord[0]
		for path in rock_paths for coord in path
	]
	ys = [
		coord[1]
		for path in rock_paths for coord in path
	]

	if any(dim < 0 for dim in xs + ys):
		raise Exception(f"Unexpected negative dim")

	max_x = max(xs)
	max_y = max(ys)

	map_state = []
	for _y in range(max_y + 1):
		row = []
		for _x in range(max_x + 1):
			row.append(".")
		map_state.append(row)

	map = TileMap(map_state)

	i = 0
	for rock_path in rock_paths:
		for start_coord, end_coord in pairwise(rock_path):
			start_coord, end_coord = list(sorted([start_coord, end_coord]))
			sx, sy = start_coord
			ex, ey = end_coord

			path_coords: Iterable[tuple[int, int]]
			if sx != ex:
				path_coords = (
					(x, sy)
					for x in range(sx, ex + 1)
				)
			else:
				path_coords = (
					(sx, y)
					for y in range(sy, ey + 1)
				)
			
			for x, y in path_coords:
				i += 1
				map.set_at(x, y, "#")

	return map

def simulate_sand(
	map: CaveMap,
	floor_height: Optional[int] = None
) -> int:
	map = copy.deepcopy(map)
	sand_source = (500, 0)

	sand_count = 0
	while True:
		if map.get_at(*sand_source) == "o":
			map.print()
			return sand_count
		
		sand_x, sand_y = sand_source
		while map.get_at(sand_x, sand_y, safe=True) == ".":
			new_pos_candidates = [
				(sand_x, sand_y + 1),
				(sand_x - 1, sand_y + 1),
				(sand_x + 1, sand_y + 1),
			]

			for new_x, new_y in new_pos_candidates:
				if floor_height is None:
					if not map.contains_coordinates(new_x, new_y):
						return sand_count
				
				elif new_y >= floor_height:
					continue
				
				if map.get_at(new_x, new_y, safe=True) == ".":
					sand_x = new_x
					sand_y = new_y
					break
			
			else:
				break
			
		map.set_at(sand_x, sand_y, "o")
		sand_count += 1

def part1(rock_paths: list[RockPath]) -> int:
	return simulate_sand(draw_map(rock_paths))

def part2(rock_paths: list[RockPath]) -> int:
	map = LazyTileMap(
		{
			(x, y): val
			for val, x, y in draw_map(rock_paths).walk()
			if val != "."
		},
		".",
	)
	floor_height = max(y for _x, y in map.state.keys()) + 2
	
	return simulate_sand(map, floor_height)
