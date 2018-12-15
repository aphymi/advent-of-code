def preprocess_input(lines):
	tracks = [list(line) for line in lines]
	
	carts = {}
	# Count up the carts.
	for y, line in enumerate(tracks):
		for x, c in enumerate(line):
			if c in "<>":
				tracks[y][x] = "-"
				carts[(x, y)] = (c, -1)
			if c in "v^":
				tracks[y][x] = "|"
				carts[(x, y)] = (c, -1)
	
	return (tracks, carts)

def get_cart_dest(tracks, carts, loc):
	x, y = loc
	if carts[loc][0] == ">":
		return ((x+1, y), tracks[y][x+1])
	elif carts[loc][0] == "<":
		return ((x-1, y), tracks[y][x-1])
	elif carts[loc][0] == "^":
		return ((x, y-1), tracks[y-1][x])
	elif carts[loc][0] == "v":
		return ((x, y+1), tracks[y+1][x])

def rotate(direc, mod=1):
	dirs = ">v<^"
	return dirs[(dirs.index(direc)+mod) % 4]

def print_tracks(tracks, carts):
	tracks = [line.copy() for line in tracks]
	for x, y in carts:
		tracks[y][x] = carts[(x, y)][0]
	
	for line in tracks:
		print("".join(line))

def sim_carts(tracks, carts, on_crash):
	next_dir = {
		(">", "-"): ">",
		(">", "/"): "^",
		(">", "\\"): "v",
		("<", "-"): "<",
		("<", "/"): "v",
		("<", "\\"): "^",
		("^", "|"): "^",
		("^", "/"): ">",
		("^", "\\"): "<",
		("v", "|"): "v",
		("v", "/"): "<",
		("v", "\\"): ">",
		
	}
			
	# Progress carts.
	while True:
		if len(carts) == 1: # Kludge workaround for part 2.
			return
		
		for cart in sorted(carts, key=lambda l: (l[1], l[0])):
			# Kludge for part 2, where carts may be deleted before the loop gets here.
			if cart not in carts:
				continue
				
			direc, inter = carts[cart]
			dest, track = get_cart_dest(tracks, carts, cart)
			if dest in carts:
				# Crash!
				x = on_crash(carts, cart, dest)
				if x:
					return x
				continue
			
			if track == "+":
				carts[dest] = (rotate(direc, inter), ((inter+2) % 3) - 1)
			else:
				carts[dest] = (next_dir[(direc, track)], inter)
				
			del carts[cart]

def part1(inp):
	tracks, carts = inp
	
	return sim_carts(tracks, carts.copy(), lambda cs, opos, npos: "{},{}".format(*npos))

def part2(inp):
	tracks, carts = inp
	carts = carts.copy()
	
	def delposs(cs, opos, npos):
		del cs[opos]
		del cs[npos]
	
	sim_carts(tracks, carts, lambda *args: delposs(*args))
	
	return "{},{}".format(*list(carts)[0])
