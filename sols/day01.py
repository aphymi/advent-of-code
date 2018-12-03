def part1(freqs):
	return str(sum(map(int, freqs)))

def part2(freqs):
	inp = list(map(int, freqs))
	cur = 0
	seen = {0}
	while True:
		for change in inp:
			cur += change
			if cur in seen:
				return cur
			seen.add(cur)
