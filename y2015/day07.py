from pprint import pprint
import re

import numpy as np

def preprocess_input(lines):
	rules = {}
	for line in lines:
		inp, out = line.split(" -> ")
		
		op = re.findall("[A-Z]+", inp)
		if not op:
			op = "ID"
		else:
			op = op[0]
		
		args = re.findall("[a-z]+|\d+", inp)
		
		rules[out] = {
			"op": op,
			"args": args,
		}
		
	return rules

def get_value(rules, wire):
	if wire.isdigit():
		return np.uint16(int(wire))
	
	rule = rules[wire]
	
	if "val" in rule:
		return rule["val"]
	
	op, args = rule["op"], rule["args"]
	
	if op == "ID":
		val = get_value(rules, args[0])
	elif op == "NOT":
		val = ~ get_value(rules, args[0])
	elif op == "OR":
		val = get_value(rules, args[0]) | get_value(rules, args[1])
	elif op == "AND":
		val = get_value(rules, args[0]) & get_value(rules, args[1])
	elif op == "RSHIFT":
		val = get_value(rules, args[0]) >> get_value(rules, args[1])
	elif op == "LSHIFT":
		val = get_value(rules, args[0]) << get_value(rules, args[1])
	else:
		raise Exception
	
	rule["val"] = val
	return val
	

def part1(rules):
	return get_value(rules, "a")

def part2(rules):
	a = get_value(rules, "a")
	for rule in rules.values():
		if "val" in rule:
			del rule["val"]
	
	rules["b"]["op"] = "ID"
	rules["b"]["args"] = (str(a),)
	
	return get_value(rules, "a")
