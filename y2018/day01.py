def preprocess_input(lines):
	return list(map(int, lines))

def part1(freqs):
	return sum(freqs)

def part2(freqs):
	cur = 0
	seen = {cur}
	while True:
		for freq in freqs:
			cur += freq
			if cur in seen:
				return cur
			seen.add(cur)
