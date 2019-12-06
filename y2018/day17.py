import time

from util.parse import *

# I find the simulation really pretty, so I'm saving this as an option to
#   watch the water flow vs just get the answer.
watch = False

def generate_clay(lines):
	clay = set()
	for dim, coords in lines:
		a, b, c = coords
		if dim == "x":
			for y in range(b, c+1):
				clay.add((a, y))
		else:
			for x in range(b, c+1):
				clay.add((x, a))
	
	return clay

parse_input = compose(
	parallel(
		map_func(lambda l: l[0]),
		get_ints,
	),
	generate_clay,
)

def printmap(clay, water, x, y):
	miny = max(0, y-10)
	maxy = y+10
	minx = x-10
	maxx = x+10
	
	map = []
	for y in range(miny, maxy+1):
		map.append([])
		for x in range(minx, maxx+1):
			if (x, y) in clay:
				map[-1].append("#")
			elif (x, y) in water:
				if water[(x, y)]:
					map[-1].append("~")
				else:
					map[-1].append("|")
			else:
				map[-1].append(".")
	
	print("\n".join("".join(row) for row in map))
	
def sim(clay):
	# Warning: On actual input, is off by 2.
	water = {} # Key is (x, y) pos; value is True if the water is settled, False otherwise.
	low_point = max(y for x, y in clay)
	high_point = min(y for x, y in clay)
	# Apparently, I'm meant to ignore any flowing water that's higher than the highest piece of clay
	#   'to prevent counting forever'. Doesn't really make sense, but whaaaatever.
	w_stack = [(500, high_point-1)] # Apparently, I'm meant to ignore any water data higher than the highest piece of clay.

	while w_stack:
		x, y = w_stack.pop()
		# Preeetttyyyyyy
		if watch:
			print()
			printmap(clay, water, x, y)
			time.sleep(.1)

		# If the water can spread down, do so.
		if (x, y+1) not in water and (x, y+1) not in clay:
			# If we haven't yet reached the low point, spread down and add to the stack.
			if y < low_point:
				# Spread downwards, keeping the current water block on the stack.
				w_stack.append((x, y))
				w_stack.append((x, y+1))
				water[(x, y+1)] = False
			
			# If we have, don't add to the stack any further.
			continue
		
		# If there's clay or settled water below, try to spread to either side.
		if water.get((x, y+1)) or (x, y+1) in clay:
			# If there's clay on the left and clay (eventually) on the right, settle the water.
			if (x-1, y) in clay:
				cx = x
				while (cx, y) in water:
					cx += 1
				if (cx, y) in clay:
					# Found more clay. Settle all the water between.
					for x_ in range(x, cx):
						water[(x_, y)] = True

			elif (x-1, y) not in water:
				# Spread out to the left.
				water[(x-1, y)] = False
				w_stack.append((x-1, y))
			
			if (x+1, y) in clay:
				cx = x
				while (cx, y) in water:
					cx -= 1

				if (cx, y) in clay:
					for x_ in range(cx+1, x+1):
						water[(x_, y)] = True

			elif (x+1, y) not in water:
				water[(x+1, y)] = False
				w_stack.append((x+1, y))
			
	return water

def part1(clay):
	return len(sim(clay))

def part2(clay):
	water = sim(clay)
	return len([w for w in water if water[w]])

