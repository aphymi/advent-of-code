from collections import defaultdict
from itertools import permutations

def preprocess_input(lines):
	prefs = defaultdict(dict)
	for line in lines:
		line = line.split()
		fst = line[0][0]
		snd = line[-1][0]
		
		prefs[fst][snd] = int(line[3]) * (-1 if line[2] == "lose" else 1)
	
	return prefs

def score(prefs, arr):
	s = prefs[arr[0]][arr[-1]] + prefs[arr[-1]][arr[0]]
	for i in range(len(arr)-1):
		s += prefs[arr[i]][arr[i+1]]
	for i in range(1, len(arr)):
		s += prefs[arr[i]][arr[i-1]]
	return s

def part1(prefs):
	return score(prefs, max(permutations(prefs.keys()), key=lambda arr: score(prefs, arr)))

def part2(prefs):
	prefs = prefs.copy()
	# noinspection PyStatementEffect
	prefs["_"] # Have to just mention it, to get it created so that the dict size doesn't change during iteration.
	for key in prefs:
		prefs[key]["_"] = 0
		prefs["_"][key] = 0
	
	return score(prefs, max(permutations(prefs.keys()), key=lambda arr: score(prefs, arr)))
