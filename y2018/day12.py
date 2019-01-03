def preprocess_input(lines):
	init = set(i for i, plant in enumerate(lines[0][15:]) if plant == "#")
		
	rules = {}
	for line in lines[2:]:
		ante, cons = line.split(" => ")
		rules[tuple(True if c == "#" else False for c in ante)] = True if cons == "#" else False
	
	return (init, rules)

def eitherside(state, ind):
	return tuple(((ind+mod) in state) for mod in (-2, -1, 0, 1, 2))

def simulate(rules, state):
	return set(pot for pot in range(min(state)-2, max(state)+3) if rules[eitherside(state, pot)])

def normalise(state):
	m = min(state)
	return set(p-m for p in state)

def part1(inp):
	state, rules = inp

	for _ in range(20):
		state = simulate(rules, state)

	return sum(state)

def part2(inp):
	state, rules = inp

	# Keep going until the pots change predictably, i.e. the new state is equal to the last,
	#   plus a constant over every pot.
	
	t = 1
	new_state = simulate(rules, state)
	
	while normalise(state) != normalise(new_state):
		t += 1
		state, new_state = new_state, simulate(rules, new_state)
	
	mod = (50000000000-t) * (min(new_state) - min(state))
	return sum(p + mod for p in new_state)

