import heapq

from util.parse import *
parse_input = compose(
	lambda inp: (inp[0][0], tuple(inp[1])),
	get_ints,
)

def around(x, y):
	return [(x+xm, y+ym) for xm, ym in ((0, 1), (0, -1), (1, 0), (-1, 0)) if 0 <= (y+ym) and 0 <= (x+xm)]

def part1(inp):
	depth, target = inp
	
	ero_levels = []
	
	def coord_to_geo_ind(x, y):
		if (x, y) in ((0, 0), target):
			return 0
		elif y == 0:
			return x*16807
		elif x == 0:
			return y*48271
		else:
			return ero_levels[y][x-1] * ero_levels[y-1][x]
	
	for y in range(target[1]+1):
		ero_levels.append([])
		for x in range(target[0]+1):
			ero_levels[-1].append((coord_to_geo_ind(x, y) + depth) % 20183)
	
	return sum(sum(el % 3 for el in row) for row in ero_levels)

def part2(inp):
	depth, target = inp
	
	# Rocky - 0 - CG | T
	# Wet - 1 - CG | N
	# Narrow - 2 - T | N
	
	# N = 0
	# T = 1
	# CG = 2
	
	# List of tuples (erosion level, type)
	region_info = [[] for _ in range(depth)]
	
	def gen_region(x, y):
		if len(region_info) <= y or len(region_info[y]) <= x:
			if (x, y) == (0, 0):
				g = 0
			elif (x, y) == target:
				gen_region(x-1, y)
				gen_region(x, y-1)
				g = 0
			elif y == 0:
				gen_region(x-1, y)
				g = x*16807
			elif x == 0:
				gen_region(x, y-1)
				g = y*48271
			else:
				gen_region(x-1, y)
				gen_region(x, y-1)
				g = region_info[y][x-1][0] * region_info[y-1][x][0]
			
			erosion = (g + depth) % 20183
			region_info[y].append((erosion, erosion % 3))
	
	# Pre-generate 'other tools', so we don't have to do it over and over again in the BFS.
	# Keys are (region type, current tool) tuples, values are the number of the tool to change to.
	otools = {
		(0, 2): 1,
		(0, 1): 2,
		(1, 0): 2,
		(1, 2): 0,
		(2, 0): 1,
		(2, 1): 0
	}
	
	# Note: Can't just use an 'explored' set. Because of how tool switching works,
	#    it's not guaranteed that the first time a location is found is the best path to that location.
	# I'm ignoring this fact for the target for the sake of simplicity, though some possible inputs probably
	#    end up not working because of that.
	best_times = {}
	# Tuples of (coord, equipped tool, minutes)
	to_explore = []
	heapq.heappush(to_explore, (0, (0, 0), 1))
	gen_region(0, 0)
	while to_explore:
		t, cur, tool = heapq.heappop(to_explore)
		
		key = (cur, tool)
		if key == (target, 1):
			return t
		
		best_times[key] = t
		
		# Try changing tool.
		otool = otools[(region_info[cur[1]][cur[0]][1], tool)]
		if best_times.get((cur, otool), float("inf")) > t+7:
			best_times[(cur, otool)] = t+7
			heapq.heappush(to_explore, (t+7, cur, otool))
		
		# Try moving around.
		for nx, ny in around(*cur):
			# Make sure it's generated.
			gen_region(nx, ny)
			if best_times.get(((nx, ny), tool), float("inf")) > t+1 and region_info[ny][nx][1] != tool:
				best_times[((nx, ny), tool)] = t+1
				heapq.heappush(to_explore, (t+1, (nx, ny), tool))
