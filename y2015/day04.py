from hashlib import md5

def preprocess_input(lines):
	return lines[0]


def valid_lead(inp, lead):
	h = md5()
	h.update(bytes(inp, "utf-8"))
	return h.hexdigest().startswith(lead)

def part1(key):
	trail = 0
	while not valid_lead(key + str(trail), "00000"):
		trail += 1
	
	return trail

def part2(key):
	
	trail = 0
	while not valid_lead(key + str(trail), "000000"):
		trail += 1
	
	return trail
