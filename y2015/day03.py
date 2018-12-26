def preprocess_input(lines):
	return lines[0]

def move(start, direc):
	x, y = start
	
	if direc == "v":
		y -= 1
	elif direc == "^":
		y += 1
	elif direc == "<":
		x -= 1
	elif direc == ">":
		x += 1
	
	return (x, y)

def part1(dirs):
	start = (0, 0)
	visited = {start}
	cur = start
	
	for direc in dirs:
		cur = move(cur, direc)
		if cur not in visited:
			visited.add(cur)

	return len(visited)

def part2(dirs):
	split_dirs = zip(dirs[::2], dirs[1::2])

	start = (0, 0)
	visited = {start}
	curs = [start, start]

	for dirs in split_dirs:
		for i in (1, 0):
			curs[i] = move(curs[i], dirs[i])
			if curs[i] not in visited:
				visited.add(curs[i])
	
	return len(visited)

