from collections import Counter
from functools import reduce

from util.parse import *

def get_minmaxes(coords):
	minx = float("inf")
	maxx = float("-inf")
	miny = float("inf")
	maxy = float("-inf")

	for x, y in coords:
		minx = min(minx, x)
		maxx = max(maxx, x)
		miny = min(miny, y)
		maxy = max(maxy, y)
	
	minmaxs = {
		"minx": minx,
		"maxx": maxx,
		"miny": miny,
		"maxy": maxy,
	}
	
	return minmaxs

parse_input = compose(lambda cs: (cs, get_minmaxes(cs)), map_func(tuple), get_ints)


def mdistance(x1, y1, x2, y2):
	return abs(x1 - x2) + abs(y1 - y2)

def closest(coords, x, y):
	closest_dist = float("inf")
	closest_coord = None
	tie = False

	for cx, cy in coords:
		dist = abs(cx-x) + abs(cy-y)
		if dist < closest_dist:
			closest_coord = (cx, cy)
			closest_dist = dist
			tie = False
		elif dist == closest_dist:
			tie = True
	
	return closest_coord if not tie else None

# TODO part1 gives an output that's too large by 1.
def part1(inp):
	coords, minmaxs = inp
	
	infinites = set()
	
	# Get coords that have infinite area.
	for x in range(minmaxs["minx"], minmaxs["maxx"]+1): # top and bottom edge
		for y in (minmaxs["miny"], minmaxs["maxy"]+1):
			infinites.add(closest(coords, x, y))
	
	for y in range(minmaxs["miny"], minmaxs["maxy"]+1): # left and right edge
		for x in (minmaxs["minx"], minmaxs["maxx"]+1):
			infinites.add(closest(coords, x, y))

	areas = Counter(coords)

	for x in range(minmaxs["minx"], minmaxs["maxx"]+1):
		for y in range(minmaxs["miny"], minmaxs["maxy"]+1):
			closest_dist = float("inf")
			closest_coord = None
			tie = False
			for cx, cy in coords:
				dist = abs(cx - x) + abs(cy - y)
				if dist < closest_dist:
					closest_coord, closest_dist = (cx, cy), dist
					tie = False
				elif dist == closest_dist:
					tie = True
			if not tie:
				areas[closest_coord] += 1
	
	for c in list(areas.keys()):
		if c in infinites:
			del areas[c]
	return max(areas.values())

def part2(inp):
	coords, minmaxs = inp
	
	safes = 0
	# Going to just assume that the safe regions stops within the adjusted region. May or may not be generally true.
	for x in range(minmaxs["minx"], minmaxs["maxx"]+1):
		for y in range(minmaxs["miny"], minmaxs["maxy"]+1):
			safes += reduce(lambda s, c: s + (abs(c[0]-x) + abs(c[1]-y)), coords, 0) < 10000
	
	return safes

