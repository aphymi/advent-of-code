import re

from util.parse import *

def action(line):
	if line.startswith("turn off"):
		return 0
	elif line.startswith("turn on"):
		return 1
	else: # line.startswith("toggle")
		return 2

parse_input = parallel(map_func(action), get_ints)

def part1(insts):
	print(insts)
	lights = [[False for _ in range(1000)] for _ in range(1000)]
	
	for act, coords in insts:
		x1, y1, x2, y2 = coords
		for x in range(x1, x2+1):
			for y in range(y1, y2+1):
				if act == 0:
					lights[x][y] = False
				elif act == 1:
					lights[x][y] = True
				else:
					lights[x][y] = not lights[x][y]
	
	return sum([sum(row) for row in lights])

def part2(insts):
	lights = [[0 for _ in range(1000)] for _ in range(1000)]

	for act, coords in insts:
		x1, y1, x2, y2 = coords
		for x in range(x1, x2+1):
			for y in range(y1, y2+1):
				if act == 0:
					lights[x][y] = max(0, lights[x][y]-1)
				elif act == 1:
					lights[x][y] += 1
				else:
					lights[x][y] += 2
	
	return sum([sum(row) for row in lights])
