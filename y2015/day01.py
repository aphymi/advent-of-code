from util.parse import *
parse_input = single_line

def part1(parens):
	return parens.count("(") - parens.count(")")

def part2(parens):
	floor = 0
	
	for i, par in enumerate(parens):
		floor += 1 if par == "(" else -1
		if floor < 0:
			return i+1
