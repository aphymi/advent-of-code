from typing import Dict, List, Tuple

import networkx as nx

from util.parse import *

# Convert input to a list of 2-tuple edges, then use them as edge input to a
# 	DiGraph.
parse_input = compose(
	nx.DiGraph,
	map_func(tuple),
	split_on(")"),
	map_func(lambda l: l.strip()),
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
