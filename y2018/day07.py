from util.parse import *

def assemble(lines):
	steps = {}
	for fst, snd in lines:
		if fst not in steps:
			steps[fst] = []
		if snd not in steps:
			steps[snd] = []
		steps[fst].append(snd)
	return steps

parse_input = compose(get_regex_matches(r"\b[A-Z]\b"), assemble)

def readys(steps, dones):
	# Filter out all the steps that are done.
	steps = {step: steps[step] for step in steps if step not in dones}
	return [step for step in steps if all([step not in steps[st] for st in steps])]

def part1(steps):
	dones = []
	while len(dones) < len(steps):
		dones.append(min(readys(steps, dones)))
	
	return "".join(dones)

def part2(steps):
	num_workers = 5
	worker_times = [("", 0)]*num_workers
	
	t = 0
	dones = []
	workings = set()
	while len(dones) < len(steps):
		for c, wt in worker_times:
			if wt <= t and c and c not in dones:
				dones.append(c)
				workings.remove(c)
		
		rs = list(reversed(sorted([r for r in readys(steps, dones) if r not in workings])))
		for i, (_, wt) in enumerate(worker_times):
			if wt <= t and rs:
				c = rs.pop()
				workings.add(c)
				worker_times[i] = (c, t + 60 + (ord(c) - 64))
		
		t = min([wt for _, wt in worker_times if wt > t], default=t)
	
	return t
