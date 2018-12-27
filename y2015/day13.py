from collections import defaultdict
from itertools import permutations

def preprocess_input(lines):
	prefs = defaultdict(int)
	for line in lines:
		line = line.split()
		prefs[(line[0], line[-1][:-1])] = int(line[3]) * (1 if line[2] == "gain" else -1)
	
	return prefs

def score(prefs, arrange):
	return sum(prefs[(a1, a2)] + prefs[(a2, a1)] for a1, a2 in zip(arrange[:-1], arrange[1:])) + \
				prefs[(arrange[-1], arrange[0])] + prefs[(arrange[0], arrange[-1])]

def part1(prefs):
	return max(score(prefs, arrange) for arrange in permutations(set(p1 for p1, p2 in prefs)))

def part2(prefs):
	prefs = prefs.copy()
	return max(score(prefs, arrange) for arrange in permutations(set(p1 for p1, p2 in prefs) | {"_"}))
