from functools import reduce

def preprocess_input(lines):
	coords = []
	for line in lines:
		(a, b) = line.split(", ")
		coords.append((int(a), int(b)))
	
	minx = float("inf")
	maxx = float("-inf")
	miny = float("inf")
	maxy = float("-inf")

	for x, y in coords:
		minx = min(minx, x)
		maxx = max(maxx, x)
		miny = min(miny, y)
		maxy = max(maxy, y)

	aminx = minx - (maxx-minx)
	aminy = miny - (maxy-miny)
	amaxx = maxx + (maxx-minx)
	amaxy = maxy + (maxy-miny)
	
	maxmins = {
		"minx": minx,
		"maxx": maxx,
		"miny": miny,
		"maxy": maxy,
		"aminx": aminx,
		"amaxx": amaxx,
		"aminy": aminy,
		"amaxy": amaxy
	}
	
	return (coords, maxmins)

def mdistance(x1, y1, x2, y2):
	return abs(x1 - x2) + abs(y1 - y2)

def closest(coords, x, y):
	closest_dist = float("inf")
	closest_coord = None
	tie = False

	for cx, cy in coords:
		dist = mdistance(cx, cy, x, y)
		if dist < closest_dist:
			closest_coord = (cx, cy)
			closest_dist = dist
			tie = False
		elif dist == closest_dist:
			tie = True
	
	return closest_coord if not tie else None

def part1(inp):
	coords, minmaxs = inp
	
	infinites = set()
	
	# Get coords that have infinite area.
	for x in range(aminx, amaxx+1): # top and bottom edge
		for y in (aminy, amaxy):
			infinites.add(closest(coords, x, y))
	
	for y in range(aminy, amaxy+1): # left and right edge
		for x in (aminx, amaxx):
			infinites.add(closest(coords, x, y))

	areas = {coord: 0 for coord in coords}

	for x in range(minx, maxx+1):
		for y in range(miny, maxy+1):
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
	for x in range(minmaxs["aminx"], minmaxs["amaxx"]+1):
		for y in range(minmaxs["aminy"], minmaxs["amaxy"]+1):
			if reduce(lambda s, c: s + mdistance(c[0], c[1], x, y), coords, 0) < 10000:
				safes += 1
	
	return safes

