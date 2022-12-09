from util.parse import *


parse_input = compose(
	split,
	map_func(lambda line: (line[0], int(line[1]))),
)

Instruction = tuple[str, int]
Coord = tuple[int, int]

def add_coords(c1: Coord, c2: Coord) -> Coord:
	return tuple(sum((c1p, c2p)) for c1p, c2p in zip(c1, c2))

def directionify(num: int) -> int:
	"""
	Convert any non-zero integer to one, with the same sign.
	"""

	if num == 0:
		return 0
	
	return int(num / abs(num))

def move_tail_to_head(head_pos: Coord, old_tail_pos: Coord) -> Coord:
	x_delta = head_pos[0] - old_tail_pos[0]
	y_delta = head_pos[1] - old_tail_pos[1]

	if abs(x_delta) <= 1 and abs(y_delta) <= 1:
		return old_tail_pos
	
	else:
		return add_coords(
			old_tail_pos,
			(directionify(x_delta), directionify(y_delta)),
		)

direction_deltas = {
	"U": (0, 1),
	"D": (0, -1),
	"R": (1, 0),
	"L": (-1, 0),
}
def get_new_head_position(head_pos: Coord, direction: str):
	return add_coords(
		head_pos,
		direction_deltas[direction],
	)

def simulate(instructions: list[Instruction], knots: int) -> int:
	knots = [(0, 0)] * knots
	last_tail_visited = {knots[-1]}

	for direction, steps in instructions:
		for _i in range(steps):
			new_knots = [get_new_head_position(knots[0], direction)]
			for tail_knot_pos in knots[1:]:
				new_knots.append(
					move_tail_to_head(
						new_knots[-1],
						tail_knot_pos,
					)
				)
			
			last_tail_visited.add(new_knots[-1])
			knots = new_knots
	
	return len(last_tail_visited)

def part1(instructions: list[Instruction]) -> int:
	return simulate(instructions, 2)

def part2(instructions: list[Instruction]) -> int:
	return simulate(instructions, 10)
