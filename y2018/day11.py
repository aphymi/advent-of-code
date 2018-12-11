def preprocess_input(lines):
	return [[((((x+11)*(y+1) + int(lines[0])) * (x+11)) // 100 % 10) - 5 for x in range(300)]
							for y in range(300)]

def grid(x, y, size):
	return [(x+xm, y+ym) for xm in range(size) for ym in range(size)]

def part1(pwls):
	maxx, maxy = max(((x, y) for x in range(298) for y in range(298)),
				  key=lambda c: sum([pwls[y_][x_] for x_, y_ in grid(c[0], c[1], 3)]))
	
	return (maxx+1, maxy+1)

def part2(pwls):
	max_power = (-1, -1, float("-inf"))
	
	for x, y in ((x, y) for x in range(300) for y in range(300)):
		cur_power = 0
		for size in range(300-max(x, y)):
			cur_power += (sum(pwls[y_][x+size] for y_ in range(y, y+size+1)) +
			              sum(pwls[y+size][x_] for x_ in range(x, x+size)))
			max_power = max(max_power, (x, y, cur_power), key=lambda p: p[2])
	
	return (max_power[0]+1, max_power[1]+1, max_power[2])
