from typing import Dict, List, Tuple

import networkx as nx

from util.parse import *

parse_input = compose(
	# Get rid of trailing newlines.
	map_func(lambda l: l.strip()),
	
	# Separate the names of the orbital bodies.
	split_on(")"),
	
	# Convert the 2-item lists into 2-tuples.
	map_func(tuple),
	
	# Make a directed graph, using the orbit list for edges.
	nx.DiGraph,
)

OrbitGraph = nx.DiGraph

def part1(orbits: OrbitGraph) -> int:
	orbit_totals: Dict[str, int] = {}
	
	for node in nx.topological_sort(orbits):
		total_node_orbits = 0
		for predecessor in orbits.predecessors(node):
			total_node_orbits += orbit_totals[predecessor] + 1
		
		orbit_totals[node] = total_node_orbits
	
	return sum(orbit_totals.values())

def part2(orbits: OrbitGraph) -> int:
	# Convert the orbit graph to be undirected.
	orbits = nx.Graph(orbits)
	
	# Subtract 2, to account for the edge from YOU to the body you're currently
	# 	orbiting, and the edge from SAN to the body he's currently orbiting.
	return nx.shortest_path_length(orbits, "YOU", "SAN") - 2
