from util.parse import *

def to_dict(line):
	return {
		"id": line[0],
		"w_offset": line[1],
		"h_offset": line[2],
		"width": line[3],
		"height": line[4],
		"w_end": line[1] + line[3],
		"h_end": line[2] + line[4],
	}

parse_input = compose(get_ints, map_func(to_dict))

def part1(claims):
	existing = set()
	dupls_found = set()

	for claim in claims:
		claim_squares = [(x, y) for x in range(claim["w_offset"], claim["w_end"])
								for y in range(claim["h_offset"], claim["h_end"])]

		for claim_square in claim_squares:
			if claim_square in existing and claim_square not in dupls_found:
				dupls_found.add(claim_square)
			else:
				existing.add(claim_square)
	
	return len(dupls_found)

def part2(claims):
	def overlap(claim1, claim2):
		w_ol = False
		for cl1, cl2 in ((claim1, claim2), (claim2, claim1)):
			w_ol = (w_ol or cl1["w_offset"] <= cl2["w_offset"] < cl1["w_end"] or
							cl1["w_offset"] < cl2["w_end"] <= cl1["w_end"])
		
		h_ol = False
		for cl1, cl2 in ((claim1, claim2), (claim2, claim1)):
			h_ol = (h_ol or cl1["h_offset"] <= cl2["h_offset"] < cl1["h_end"] or
							cl1["h_offset"] < cl2["h_end"] <= cl1["h_end"])
		
		return w_ol and h_ol
	
	for claim1 in claims:
		for claim2 in claims:
			if claim1 is not claim2 and overlap(claim1, claim2):
				break
				
		else:
			# Theoretically, if the input precondition is to be believed, there should be exactly one claim that doesn't overlap.
			return claim1["id"]
