import re

def preprocess_input(lines):
	instructions = []
	for line in lines:
		if line.startswith("toggle"):
			action = 2
		elif line.startswith("turn on"):
			action = 1
		else:
			action = 0
		instructions.append([action] + list(map(int, re.findall("\d+", line))))
	
	return instructions

def part1(insts):
	lights = [[False for _i in range(1000)] for _j in range(1000)]
	
	for act, x1, y1, x2, y2 in insts:
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
	lights = [[0 for _i in range(1000)] for _j in range(1000)]
	
	for act, x1, y1, x2, y2 in insts:
		for x in range(x1, x2+1):
			for y in range(y1, y2+1):
				if act == 0:
					if lights[x][y] > 0:
						lights[x][y] -= 1
				elif act == 1:
					lights[x][y] += 1
				else:
					lights[x][y] += 2
	
	return sum([sum(row) for row in lights])
