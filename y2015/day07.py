import numpy as np

def parse_input(lines):
	rules = {}
	for line in lines:
		inp, out = line.split(" -> ")
		inp = inp.split()
		
		if len(inp) == 1:
			rules[out] = {"op": None, "args": inp}
			
		elif len(inp) == 2:
			rules[out] = {"op": inp[0], "args": inp[1:]}
		
		else: # len(inp) == 3
			rules[out] = {"op": inp[1], "args": (inp[0], inp[2])}
		
	return rules

wire_cache = {}
def get_value(rules, wire):
	if wire in wire_cache:
		return wire_cache[wire]
	
	if wire.isdigit():
		return np.uint16(int(wire))
	
	rule = rules[wire]
	
	op, args = rule["op"], rule["args"]
	
	if op == "NOT":
		val = ~ get_value(rules, args[0])
	elif op == "OR":
		val = get_value(rules, args[0]) | get_value(rules, args[1])
	elif op == "AND":
		val = get_value(rules, args[0]) & get_value(rules, args[1])
	elif op == "RSHIFT":
		val = get_value(rules, args[0]) >> get_value(rules, args[1])
	elif op == "LSHIFT":
		val = get_value(rules, args[0]) << get_value(rules, args[1])
	else: # op == None
		val = get_value(rules, args[0])
	
	wire_cache[wire] = val
	return val
	

def part1(rules):
	try:
		return get_value(rules, "a")
	finally:
		wire_cache.clear()

def part2(rules):
	try:
		a = get_value(rules, "a")
		wire_cache.clear()
		wire_cache["b"] = a
		return get_value(rules, "a")
	finally:
		wire_cache.clear()
