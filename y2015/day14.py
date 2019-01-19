from collections import defaultdict

from util.parse import *
parse_lines = compose(dictify, parallel(map_func(lambda l: l[:l.index(" ")]), get_ints))

def preprocess_input(lines):
	deer = {}
	for line in lines:
		deer[line[:line.index(" ")]] = tuple(map(int, re.findall(r"\d+", line)))
	
	return deer

def distance(deerinfo, time):
	speed, dur, rest = deerinfo
	dist = (speed*dur) * (time // (dur+rest))
	rem = time % (dur+rest)
	if rem < dur:
		dist += speed * rem
	else:
		dist += speed * dur
	
	return dist

def part1(deer):
	return max(distance(d, 2503) for d in deer.values())

def part2(deer):
	points = defaultdict(int)
	
	for t in range(1, 2504):
		dists = [(dname, distance(dinfo, t)) for dname, dinfo in deer.items()]
		maxd = max(dist for _, dist in dists)
		for dname, dist in dists:
			if dist == maxd:
				points[dname] += 1
	
	return max(points.values())
