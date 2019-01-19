from util.parse import *
parse_input = map_func(list)

def adj(cur_map, x, y):
	return [cur_map[y+ym][x+xm] for xm in (-1, 0, 1)
								for ym in (-1, 0, 1)
							if (xm, ym) != (0, 0) and
							   0 <= y+ym < len(cur_map) and
							   0 <= x+xm < len(cur_map[y+ym])]

def step(cur_map):
	new_map = []
	for y, row in enumerate(cur_map):
		new_map.append([])
		for x, space in enumerate(row):
			adjac = adj(cur_map, x, y)
			if space == ".":
				new_map[-1].append("|" if adjac.count("|") >= 3 else ".")
			
			elif space == "|":
				new_map[-1].append("#" if adjac.count("#") >= 3 else "|")

			else:
				new_map[-1].append("#" if "|" in adjac and "#" in adjac else ".")
	
	return new_map

def value(cur_map):
	return sum(row.count("|") for row in cur_map) * sum(row.count("#") for row in cur_map)
		

def part1(cur_map):
	for _ in range(10):
		cur_map = step(cur_map)
	
	return value(cur_map)

def part2(cur_map):
	# Look for a state we see twice in a row.
	seen = set()
	cycle = []
	t = 0
	while True:
		cur_map = step(cur_map)
		if cycle:
			if cur_map == cycle[0]:
				break
			cycle.append(cur_map)
		else:
			tup = tuple(tuple(row) for row in cur_map)
			if tup in seen:
				cycle.append(cur_map)
			else:
				seen.add(tup)
		t += 1

	final_map = cycle[(1000000000 - 1 - t) % len(cycle)]
	return value(final_map)

