from util.parse import *
from util.tile_map import TileMap


parse_input = compose(
	map_func(lambda line: [int(c) for c in line]),
	TileMap,
)

Coords = tuple[int, int]
TreeGrid = TileMap[int]
TreeMap = list[list[int]]

def transpose(tree_map: TreeMap) -> TreeGrid:
	return [
		[
			tree_map.get_at(x, y)
			for y in range(tree_map.get_height())
		]
		for x in range(tree_map.get_width())
	]

def get_trees_visible_from(tree_map: TreeMap, direction: str) -> list[Coords]:
	delta: int
	is_transposed = False
	tree_grid: TreeGrid
	if direction in ("north", "south"):
		tree_grid = transpose(tree_map)
		is_transposed = True
		delta = 1 if direction == "north" else -1
	
	elif direction in ("west", "east"):
		tree_grid = tree_map.state
		delta = 1 if direction == "west" else -1
	
	else:
		raise Exception(f"Bad direction: {direction}")
	
	visible_trees = []
	for y, row in enumerate(tree_grid):
		row_indices = range(0, len(row))
		if delta == -1:
			row_indices = reversed(row_indices)

		tallest_tree_seen = -float("inf")
		for x in row_indices:
			tree_height = tree_grid[y][x]
			if tree_height > tallest_tree_seen:
				tallest_tree_seen = tree_height

				visible_trees.append(
					(y, x) if is_transposed else (x, y)
				)
	
	return visible_trees

def add_coords(c1: Coords, c2: Coords) -> Coords:
	return (c1[0] + c2[0], c1[1] + c2[1])

def get_sightline_from(
	tree_map: TreeMap,
	x: int,
	y: int,
	direction: str,
) -> int:
	delta = {
		"north": (0, -1),
		"south": (0, 1),
		"west": (-1, 0),
		"east": (1, 0),
	}[direction]

	sightline = 0
	to_check = (x, y)
	while True:
		to_check = add_coords(to_check, delta)
		if not tree_map.contains_coordinates(*to_check):
			break
		
		sightline += 1
		if tree_map.get_at(*to_check) >= tree_map.get_at(x, y):
			break
	
	return sightline

def get_scenic_score(tree_map: TreeMap, x: int, y: int) -> int:
	return (
		get_sightline_from(tree_map, x, y, "north")
		* get_sightline_from(tree_map, x, y, "south")
		* get_sightline_from(tree_map, x, y, "west")
		* get_sightline_from(tree_map, x, y, "east")
	)

def part1(tree_map: TreeMap) -> int:
	return len(
		set(
			get_trees_visible_from(tree_map, "north")
		).union(
			get_trees_visible_from(tree_map, "south")
		).union(
			get_trees_visible_from(tree_map, "west")
		).union(
			get_trees_visible_from(tree_map, "east")
		)
	)

def part2(tree_map: TreeGrid) -> int:
	return max(
		get_scenic_score(tree_map, x, y)
		for _tree_height, x, y in tree_map.walk()
	)
