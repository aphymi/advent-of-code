from collections import defaultdict, deque
import re

def preprocess_input(lines):
	return construct_rooms(lines[0][1:-1])

def follow_dir(adj_rooms, x, y, direc):
	if direc == "N":
		end = (x, y+1)
	elif direc == "S":
		end = (x, y-1)
	elif direc == "W":
		end = (x-1, y)
	else:
		end = (x+1, y)
	
	adj_rooms[(x, y)].add(end)
	adj_rooms[end].add((x, y))
	return end
	

def construct_rooms(directions):
	adj_rooms = defaultdict(set)
	
	# | is intentionally left out of here. It just breaks up \w+, and is otherwise not needed.
	#   The string '|(' does not exist anywhere in the regex.
	chunks = re.findall(r"\w+|[()]|\|+", directions + ")")
	
	def parse(cur):
		parts = [[]]
		while True:
			if chunks[cur] == "|":
				parts.append([])
			
			elif chunks[cur] == "(":
				cur, part = parse(cur+1)
				parts[-1].append(part)
			
			elif chunks[cur] == ")":
				# Empty pipe part only ever comes at end of capture group.
				if not parts[-1]:
					parts[-1].append("")
				return cur, parts
			
			else:
				parts[-1].append(chunks[cur])
			
			cur += 1
	
	parts = parse(0)[1]
	
	# Note: The first character in the regex must not be a (.
	
	def follow_ppart(ppart, strt):
		curs = {strt}
		for part in ppart:
			new_curs = set()
			if isinstance(part, str):
				for cur in curs:
					for direc in part:
						cur = follow_dir(adj_rooms, *cur, direc)
					new_curs.add(cur)
			else:
				for cur in curs:
					for pp in part:
						new_curs |= follow_ppart(pp, cur)
			curs = new_curs
		
		return curs
	
	for pp in parts:
		follow_ppart(pp, (0, 0))
	
	return adj_rooms
	

def part1(adj_rooms):
	# Do a bfs, and return the very last thing found.
	found = set()
	to_explore = deque()
	to_explore.appendleft(((0, 0), 0))
	while to_explore:
		cur, dist = to_explore.pop()
		for adj_room in adj_rooms[cur]:
			if adj_room not in found:
				found.add(adj_room)
				to_explore.appendleft((adj_room, dist+1))
	
	return dist

def part2(adj_rooms):
	# Do a bfs, keeping track of rooms with distance > 1000
	far_rooms = 0
	found = set()
	to_explore = deque()
	to_explore.appendleft(((0, 0), 0))
	while to_explore:
		cur, dist = to_explore.pop()
		if dist >= 1000:
			far_rooms += 1
		for adj_room in adj_rooms[cur]:
			if adj_room not in found:
				found.add(adj_room)
				to_explore.appendleft((adj_room, dist+1))
	
	return far_rooms
