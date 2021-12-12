import copy
from functools import cache

import networkx as nx

from util.parse import *


parse_input = compose(
	split_on("-"),
	map_func(tuple),
	nx.Graph,
)


@cache
def find_paths_between(
	graph: nx.graph,
	start: str,
	end: str,
	visited: frozenset[str],
	already_visited_twice: bool = True
):
	paths = set()

	is_revisitable = start.isupper()

	new_visited = visited if is_revisitable else visited.union({start})

	for neighbor in graph.neighbors(start):
		if neighbor == end:
			paths.add((start, end))
			continue

		if neighbor in visited:
			continue

		continued_paths = find_paths_between(
			graph,
			neighbor,
			end,
			new_visited,
			already_visited_twice
		)
		for path in continued_paths:
			paths.add((start, *path))
		
		can_revisit_small_self = (
			start != "start"
			and not is_revisitable
			and not already_visited_twice
		)
		
		if can_revisit_small_self:
			more_continued_paths = find_paths_between(
				graph,
				neighbor,
				end,
				visited,
				True,
			)
			for path in more_continued_paths:
				paths.add((start, *path))

	return paths

def part1(graph: nx.Graph) -> int:
	paths = find_paths_between(
		graph,
		"start",
		"end",
		frozenset()
	)

	return len(paths)

def part2(graph: nx.Graph) -> int:
	paths = find_paths_between(
		graph,
		"start",
		"end",
		frozenset(),
		False
	)

	return len(paths)
