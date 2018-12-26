def preprocess_input(lines):
	return [tuple(map(int, line.split(","))) for line in lines]

def m_dist(pos1, pos2):
	return sum(abs(c1 - c2) for c1, c2 in zip(pos1, pos2))

def part1(coords):
	coords = set(coords)
	constellations = 0
	
	while coords:
		coord = coords.pop()
		constellations += 1
		# Pop off all in the same constellation.
		to_explore = [coord]
		while to_explore:
			nc = to_explore.pop()
			if nc in coords:
				coords.remove(nc)
			
			to_explore.extend(c for c in coords if m_dist(nc, c) <= 3)
	
	return constellations

def part2(_):
	return "DNE"
