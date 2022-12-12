import heapq
from typing import Optional

from util.parse import *
from util.tile_map import TileMap


parse_input = lambda lines: TileMap([list(line) for line in lines])

def get_shortest_path(
	map: TileMap[str],
	start: tuple[int, int],
) -> Optional[int]:
	visited = set()
	queue = [(0, start[0], start[1])]

	while len(queue) > 0:
		steps, cx, cy = heapq.heappop(queue)
		if (cx, cy) in visited:
			continue

		visited.add((cx, cy))

		cur_height = map.get_at(cx, cy)
		if cur_height == "E":
			return steps
		
		if cur_height == "S":
			cur_height = "a"

		for height, x, y in map.get_adjacent_4(cx, cy):
			if (x, y) in visited:
				continue
			
			if height == "E":
				height = "z"

			if ord(height) - 1 <= ord(cur_height):
				heapq.heappush(queue, (steps + 1, x, y))
	
	return None

def part1(map: TileMap[str]) -> int:
	start = next(
		(x, y)
		for height, x, y in map.walk()
		if height == "S"
	)
	return get_shortest_path(map, start)

def part2(map: TileMap[str]) -> int:
	valid_trail_lengths = []
	for height, x, y in map.walk():
		if height not in ("S", "a"):
			continue
		
		path_length = get_shortest_path(map, (x, y))
		if path_length is not None:
			valid_trail_lengths.append(path_length)
	
	return min(valid_trail_lengths)
