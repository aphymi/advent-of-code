from collections import defaultdict

def preprocess_input(lines):
	init = defaultdict(bool)
	for i, plant in enumerate(lines[0][15:]):
		init[i] = True if plant == "#" else False

	rules = {}
	for line in lines[2:]:
		ante, cons = line.split(" => ")
		rules[tuple(True if c == "#" else False for c in ante)] = True if cons == "#" else False
	
	return (init, rules)

def eitherside(state, ind):
	return (state[ind-2], state[ind-1], state[ind], state[ind+1], state[ind+2])

def simulate(rules, state):
	new_state = state.copy()

	for pot_num in range(min(state)-2, max(state)+3):
		new_state[pot_num] = rules[eitherside(state, pot_num)]
	
	return new_state 

def pretty(state):
	new_state = []
	for i in range(min(state), max(state)+1):
		new_state.append("#" if state[i] else ".")
	
	return "".join(new_state)

def part1(inp):
	state, rules = inp

	for _ in range(20):
		state = simulate(rules, state)

	return sum([key for key, value in state.items() if value])

def part2(inp):
	state, rules = inp

	# Assume that, after 200 iterations, the state is stable.
	# Once it's stable, the only change is moving to the right by one every iteration.

	for _ in range(200):
		state = simulate(rules, state)
	
	# Trim the state
	#i = min(state)
	#while not state[i]:
	#	del state[i]
	#	i += 1
	
	#i = max(state)
	#while not state[i]:
	#	del state[i]
	#	i -= 1
	
	mod = 50000000000 - 200
	new_state = {}
	for key in state:
		new_state[key+mod] = state[key]
	
	return sum([key for key, value in new_state.items() if value])

