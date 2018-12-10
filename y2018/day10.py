import re

def preprocess_input(lines):
	lights = []
	for line in lines:
		lights.append(list(map(int, re.findall("-?\d+", line))))
	
	return lights

def minmax_poses(poses):
	minx = miny = float("inf")
	maxx = maxy = float("-inf")
	for pos in poses:
		minx = min(minx, pos[0])
		maxx = max(maxx, pos[0])
		miny = min(miny, pos[1])
		maxy = max(maxy, pos[1])
	
	return (minx, maxx, miny, maxy)

_msg_t = []
def find_msg_t(lights):
	# The solution should be cached, since this is a lot of work.
	if _msg_t:
		return _msg_t[0]
	
	# Search for the t with the minimum bounding box.
	poses = [[px, py] for px, py, vx, vy in lights]
	vels = [(vx, vy) for px, py, vx, vy in lights]
	
	min_area = float("inf")
	min_t = -1
	# Assume that it happens in the first eleven-thousand seconds.
	for t in range(11000):
		minx, maxx, miny, maxy = minmax_poses(poses)
		
		# Assume that the smallest-area hull is the message.
		area = (maxx-minx) * (maxy-miny)
		if area < min_area:
			min_area = area
			min_t = t
	
		for i in range(len(poses)):
			poses[i][0] += vels[i][0]
			poses[i][1] += vels[i][1]
	
	_msg_t.append(min_t)
	return min_t
	
def part1(lights):
	msg_t = find_msg_t(lights)

	poses = [(px + vx*msg_t, py + vy*msg_t) for px, py, vx, vy in lights]
	minx, maxx, miny, maxy = minmax_poses(poses)
	
	chars = []
	for y in range(int(maxy - miny)+1):
		chars.append("\n")
		for x in range(int(maxx - minx)+1):
			if (x+minx, y+miny) in poses:
				chars.append("#")
			else:
				chars.append(" ")
	
	return "".join(chars)

def part2(lights):
	return find_msg_t(lights)
