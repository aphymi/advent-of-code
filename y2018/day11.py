from util.parse import *

def gen_sat(serial):
	pwls = [[((((x + 11) * (y + 1) + serial) * (x + 11)) // 100 % 10) - 5 for y in range(300)]
			for x in range(300)]
	
	sat = [[0 for _ in range(300)] for _ in range(300)]
	
	for x, y in ((x, y) for x in range(300) for y in range(300)):
		sat[x][y] = pwls[x][y]
		if x > 0:
			sat[x][y] += sat[x - 1][y]
		if y > 0:
			sat[x][y] += sat[x][y - 1]
		if x > 0 and y > 0:
			sat[x][y] -= sat[x - 1][y - 1]
	
	return sat

parse_input = compose(single_line, int, gen_sat)

def grid_power(sat, x, y, size):
	a = sat[x-1][y-1] if x > 0 and y > 0 else 0
	b = sat[x+size-1][y-1] if y > 0 else 0
	c = sat[x-1][y+size-1] if x > 0 else 0
	d = sat[x+size-1][y+size-1]
	return d + a - b - c


def part1(sat):
	maxx, maxy = max(((x, y) for x in range(298) for y in range(298)),
				   key=lambda c: grid_power(sat, c[0], c[1], 3))
	
	return (maxx + 1, maxy + 1)


def part2(sat):
	maxx, maxy, maxs = max(((x, y, s) for x in range(300)
									  for y in range(300)
									  for s in range(1, 301-max(x, y))),
						   key=lambda c: grid_power(sat, *c))
	
	return (maxx+1, maxy+1, maxs)
