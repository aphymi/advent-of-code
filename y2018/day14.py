def preprocess_input(lines):
	return lines[0]

def sim(recs, fst, snd):
	for c in str(recs[fst] + recs[snd]):
		recs.append(int(c))
		
	return [(x + recs[x] + 1) % len(recs) for x in (fst, snd)]

def part1(num_recs):
	num_recs = int(num_recs)
	recs = [3, 7]
	
	fst = 0
	snd = 1
	
	while len(recs) < num_recs+10:
		fst, snd = sim(recs, fst, snd)
		
	return "".join(map(str, recs[-10:]))

def part2(recs_subs):
	recs_subs = list(int(c) for c in recs_subs)
	print(recs_subs)
	recs = [3, 7]
	fst = 0
	snd = 1
	
	while recs_subs not in (recs[-len(recs_subs):], recs[-len(recs_subs)-1:-1]):
		fst, snd = sim(recs, fst, snd)
	
	print(recs[-10:])
	if recs_subs == recs[-len(recs_subs):]:
		return len(recs) - len(recs_subs)
	else:
		return len(recs) - len(recs_subs) - 1
