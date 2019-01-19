from collections import deque

from util.parse import *
parse_input = map_func(list)

def get_unit_by_pos(units, y, x):
	for unit in units:
		if unit["pos"] == (y, x):
			return unit

def around(y, x):
	return ((y+ym, x+xm) for ym, xm in ((0, 1), (0, -1), (1, 0), (-1, 0)))

def free_around(cave_map, y, x):
	return ((ny, nx) for ny, nx in around(y, x)
				if cave_map[ny][nx] == ".")

def closest(cave_map, dests, y, x):
	if (y, x) in dests:
		return (y, x)
	
	min_dist = float("inf")
	to_explore = deque()
	for p in free_around(cave_map, y, x):
		to_explore.append((p, 1))
	explored = set()
	sols = []
	
	while to_explore:
		pos, dist = to_explore.popleft()
		if dist > min_dist:
			break
		if pos in dests:
			min_dist = dist
			sols.append(pos)
		for fpos in free_around(cave_map, pos[0], pos[1]):
			if fpos not in explored:
				explored.add(fpos)
				to_explore.append((fpos, dist+1))
	
	return min(sols) if sols else None


def simulate(cave_map, eatt, gatt):
	cave_map = [row.copy() for row in cave_map]
	units = []
	t = 0
	
	for y, row in enumerate(cave_map):
		for x, space in enumerate(row):
			if space in "EG":
				units.append({"pos": (y, x),
							  "hp": 200,
							  "group": space})
	
	while True:
		
		for unit in sorted(units, key=lambda u: u["pos"]):
			# If the unit is dead, skip its turn.
			if unit["hp"] <= 0:
				continue
			
			en_sym = "G" if unit["group"] == "E" else "E"
			# Get a list of all living enemies.
			enemies = [u for u in units if u["group"] == en_sym and u["hp"] > 0]
			
			# If no enemies are found, combat has reached its end.
			if not enemies:
				return (t, units)
			
			# Movement phase. If not already in range of a target, move towards such a range.
			enemy_ranges = set()
			enemy_adj = set()
			for enemy in enemies:
				enemy_ranges |= set(free_around(cave_map, *enemy["pos"]))
				enemy_adj |= set(around(*enemy["pos"]))
			
			# If the unit is not in range of an enemy, try to move towards one.
			if unit["pos"] not in enemy_adj:
				nearest_enemy_range = closest(cave_map, enemy_ranges, *unit["pos"])
				# If any enemy ranges are accessible, move toward one.
				if nearest_enemy_range:
					my, mx = closest(cave_map, list(free_around(cave_map, *unit["pos"])), *nearest_enemy_range)
					
					# Update to new position.
					cave_map[unit["pos"][0]][unit["pos"][1]] = "."
					cave_map[my][mx] = unit["group"]
					unit["pos"] = (my, mx)
			
			# Movement phase done.
			
			# Attack phase.:
			ir_enemies = [get_unit_by_pos(enemies, ey, ex) for ey, ex in sorted(around(*unit["pos"]))
								if cave_map[ey][ex] == en_sym]
			
			if ir_enemies:
				# Attack the in-range enemy with the lowest hp.
				enemy = min(ir_enemies, key=lambda e: e["hp"])
				
				enemy["hp"] -= eatt if unit["group"] == "E" else gatt
				if enemy["hp"] <= 0:
					cave_map[enemy["pos"][0]][enemy["pos"][1]] = "."
		
		t += 1


def part1(cave_map):
	t, units = simulate(cave_map, 3, 3)
	return t * sum(u["hp"] for u in units if u["hp"] > 0)

def part2(cave_map):
	eatt = 4
	t, units = simulate(cave_map, eatt, 3)
	while any(u["group"] == "E" and u["hp"] <= 0 for u in units):
		eatt += 1
		t, units = simulate(cave_map, eatt, 3)
	
	return t * sum(u["hp"] for u in units if u["hp"] > 0)
