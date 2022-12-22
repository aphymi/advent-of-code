from collections import deque
import itertools
from typing import Generator

from util.parse import *


parse_input = get_ints

CubeCoord = tuple[int, int, int]
CubeState = list[list[list[bool]]]

def add_coords(c1: CubeCoord, c2: CubeCoord) -> CubeCoord:
	return tuple(
		c1p + c2p
		for c1p, c2p in zip(c1, c2)
	)

def get_adjacent(x: int, y: int, z: int) -> Generator[CubeCoord, None, None]:
	adj = (
		(-1, 0, 0),
		(1, 0, 0),
		(0, -1, 0),
		(0, 1, 0),
		(0, 0, -1),
		(0, 0, 1),
	)

	for adj_delta in adj:
		yield add_coords((x, y, z), adj_delta)

def make_state(cubes: list[CubeCoord]) -> CubeState:
	max_x, max_y, max_z = [
		max(c)
		for c in zip(*cubes)
	]
	state = [
		[
			[
				False
				for _x in range(max_x + 1)
			]
			for _y in range(max_y + 1)
		]
		for _z in range(max_z + 1) 
	]

	for x, y, z in cubes:
		state[z][y][x] = True
	
	return state

def is_out_of_bounds(state: CubeState, x: int, y: int, z: int) -> bool:
	return (
		any(c < 0 for c in (x, y, z))
		or z >= len(state)
		or y >= len(state[0])
		or x >= len(state[0][0])
	)

def open_faces(state: CubeState, x: int, y: int, z: int) -> int:
	if not state[z][y][x]:
		return 0
	
	open_faces = 0
	for adj_x, adj_y, adj_z in get_adjacent(x, y, z):
		if is_out_of_bounds(state, adj_x, adj_y, adj_z):
			open_faces += 1

		elif not state[adj_z][adj_y][adj_x]:
			open_faces += 1
	
	return open_faces

def get_exposed(state: CubeState) -> set[CubeCoord]:
	z_dim = len(state)
	y_dim = len(state[0])
	x_dim = len(state[0][0])

	outside_coords = itertools.chain(
		((-1, y, z) for y in range(0, y_dim + 1) for z in range(0, z_dim + 1)),
		((x_dim, y, z) for y in range(0, y_dim + 1) for z in range(0, z_dim + 1)),
		((x, -1, z) for x in range(0, x_dim + 1) for z in range(0, z_dim + 1)),
		((x, y_dim, z) for x in range(0, x_dim + 1) for z in range(0, z_dim + 1)),
		((x, y, -1) for x in range(0, x_dim + 1) for y in range(0, y_dim + 1)),
		((x, y, z_dim) for x in range(0, x_dim + 1) for y in range(0, y_dim + 1)),
	)
	queue = deque(outside_coords)
	exposed = set()

	while len(queue) > 0:
		x, y, z = queue.popleft()

		for adj_x, adj_y, adj_z in get_adjacent(x, y, z):
			add_adj = (
				not is_out_of_bounds(state, adj_x, adj_y, adj_z)
				and not state[adj_z][adj_y][adj_x]
				and not (adj_x, adj_y, adj_z) in exposed
			)
			if add_adj:
				queue.append((adj_x, adj_y, adj_z))
				exposed.add((adj_x, adj_y, adj_z))
	
	return exposed

def part1(cubes: list[CubeCoord]) -> int:
	state = make_state(cubes)
	
	return sum(
		open_faces(state, x, y, z)
		for x, y, z in cubes
	)

def part2(cubes: list[CubeCoord]) -> int:
	state = make_state(cubes)

	exposed_coords = get_exposed(state)
	for z, plane in enumerate(state):
		for y, row in enumerate(plane):
			for x, _occupied in enumerate(row):
				if (x, y, z) not in exposed_coords:
					state[z][y][x] = True
	
	return sum(
		open_faces(state, x, y, z)
		for x, y, z in cubes
	)
