import networkx as nx

from util.parse import *
from util import tile_map


Coords = tuple[int, int]
CaveMap = tile_map.TileMap[int]

def parse_input(
	lines: list[str],
) -> CaveMap:
	return tile_map.TileMap([
		[int(c) for c in row]
		for row in lines
	])

def get_shortest_path_from(
	cave_map: CaveMap,
	start: Coords,
	end: Coords,
) -> list[Coords]:
	graph = nx.DiGraph()

	for _value, x, y in cave_map.walk():
		for adj_value, adj_x, adj_y in cave_map.get_adjacent_4(x, y):
			graph.add_edge((x, y), (adj_x, adj_y), weight=adj_value)
	
	path = nx.dijkstra_path(graph, start, end, weight="weight")

	return path

def get_path_score(cave_map: CaveMap, path: list[Coords]) -> int:
	return sum(
		cave_map.get_at(x, y)
		for x, y in path[1:]
	)

def part1(cave_map: CaveMap) -> int:
	path = get_shortest_path_from(
		cave_map,
		(0, 0),
		(
			len(cave_map.state[-1]) - 1,
			len(cave_map.state) - 1,
		)
	)

	return get_path_score(cave_map, path)

def expand_map(cave_map: CaveMap) -> CaveMap:
	x_length = len(cave_map.state[0])
	y_length = len(cave_map.state)

	def get_new_value(cave_map: CaveMap, x: int, y: int) -> int:
		x_div, x_mod = divmod(x, len(cave_map.state[0]))
		y_div, y_mod = divmod(y, len(cave_map.state))

		new_value = (cave_map.get_at(x_mod, y_mod) + x_div + y_div)

		while new_value > 9:
			new_value -= 9

		return new_value

	return tile_map.TileMap([
		[
			get_new_value(cave_map, x, y)
			for x in range(x_length * 5)
		]
		for y in range(y_length * 5)
	])

def part2(cave_map: CaveMap) -> int:
	new_map = expand_map(cave_map)

	return get_path_score(
		new_map,
		get_shortest_path_from(
			new_map,
			(0, 0),
			(
				len(new_map.state[-1]) - 1,
				len(new_map.state) - 1,
			)
		)
	)
