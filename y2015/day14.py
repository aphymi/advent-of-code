from collections import defaultdict
import re

def preprocess_input(lines):
	deer = {}
	for line in lines:
		# Deer can fly 3 km/s for 6 seconds, but then must rest for -2 seconds.
		deer[line[:line.index(" ")]] = tuple(map(int, re.findall(r"\d+", line)))
	
	print(deer)
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
