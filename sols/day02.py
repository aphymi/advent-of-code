def part1(ids):
	def char_freqs(box_id):
		freqs = {}
		
		for char in box_id:
			if char in freqs:
				freqs[char] += 1
			else:
				freqs[char] = 1
		
		return freqs
	
	twos = 0
	threes = 0
	
	for box_id in ids:
		cfreqs = char_freqs(box_id).values()
		if 2 in cfreqs:
			twos += 1
		if 3 in cfreqs:
			threes += 1
	
	return twos*threes

def part2(ids):
	check_ids = set()
	for box_id in ids:
		for i in range(len(box_id)):
			# Replace the character at the index with an underscore.
			check = box_id[:i] + "_" + box_id[i+1:]
			if check in check_ids:
				return check.replace("_", "")
			check_ids.add(check)
