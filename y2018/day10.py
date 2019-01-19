from util.parse import *
parse_input = get_ints

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
	# Cache the solution, since this is a lot of work.
	if _msg_t:
		return _msg_t[0]
	
	# Search for the t with the minimum bounding box.
	poses = [[px, py] for px, py, vx, vy in lights]
	vels = [(vx, vy) for px, py, vx, vy in lights]
	
	t = -1
	last_area = float("inf")
	while True:
		t += 1
		minx, maxx, miny, maxy = minmax_poses(poses)
		
		# Assume that the last second in which the bounding box decreases in size is the right second.
		area = (maxx-minx) * (maxy-miny)
		if area > last_area:
			break
		last_area = area
	
		for i in range(len(poses)):
			poses[i][0] += vels[i][0]
			poses[i][1] += vels[i][1]
	
	_msg_t.append(t-1)
	return t - 1
	
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
