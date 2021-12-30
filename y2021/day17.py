from util.parse import *
from util.typing import Coords


parse_input = compose(
	get_ints,
	single_line,
	lambda c: ((c[0], c[1]), (c[2], c[3]))
)

TargetRange = tuple[Coords, Coords]

def simulate(target_coords: TargetRange, vx: int, vy: int) -> None:
	steps = 100
	posx = 0
	posy = 0
	reached = set()

	for _i in range(steps):
		posx += vx
		posy += vy
		reached.add((posx, posy))

		vx -= 0 if vx == 0 else vx / abs(vx)
		vy -= 1

	(tx1, tx2), (ty1, ty2) = target_coords

	tx1, tx2 = sorted((tx1, tx2))
	ty1, ty2 = sorted((ty1, ty2))
	
	for y in range(ty2 + 10, ty1 - 10, -1):
		for x in range(tx1 - 20, tx2 + 10):
			if (x, y) == (0, 0):
				print("S", end="")
			elif (x, y) in reached:
				print("#", end="")
			elif x in range(tx1, tx2+1) and y in range(ty1, ty2+1):
				print("T", end="")
			else:
				print(".", end="")
		print()
	print()

def within_range(n: float, rnge: tuple[float, float]):
	return rnge[0] <= n <= rnge[1]

def intersects(
	vx: int,
	vy: int,
	target_range: TargetRange,
) -> bool:
	(tx1, tx2), (ty1, ty2) = target_range
	
	px = 0
	py = 0
	while True:
		px += vx
		py += vy

		if within_range(px, (tx1, tx2)) and  within_range(py, (ty1, ty2)):
			return True
		
		if vx == 0 and px not in range(tx1, tx2 + 1):
			break
		
		if vy < 0 and py < ty1:
			break

		vx -= 0 if vx == 0 else vx / abs(vx)
		vy -= 1
	
	return False

def part1(target_range: TargetRange) -> int:
	(_tx1, _tx2), (ty1, _ty2) = target_range

	max_vy = abs(ty1) - 1

	return sum(range(max_vy + 1))

def part2(target_range: TargetRange) -> int:
	(_tx1, tx2), (ty1, _ty2) = target_range

	min_vx = 0
	max_vx = tx2
	
	max_vy = abs(ty1) + 1
	min_vy = -max_vy
	
	intersections = 0
	inters = set()
	for vx in range(min_vx, max_vx + 1):
		for vy in range(min_vy, max_vy + 1):
			if intersects(vx, vy, target_range):
				intersections += 1
				inters.add((vx, vy))
	
	return intersections


