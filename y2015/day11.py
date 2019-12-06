import re

from util.parse import *

parse_input = compose(single_line, list)

def increment_pass(psswd):
	for i in range(len(psswd)-1, -1, -1):
		if psswd[i] != "z":
			psswd[i] = chr(ord(psswd[i])+1)
			break
		psswd[i] = "a"
	
def part1(psswd):
	def passes(pss):
		return any(ord(pss[i]) == ord(pss[i+1])-1 == ord(pss[i+2])-2 for i in range(len(pss)-2)) \
			and re.match(r"[^iol]+", "".join(pss)) \
			and re.match(r".*(.)\1.*(.)\2.*", "".join(pss))
	
	while not passes(psswd):
		increment_pass(psswd)
	
	return "".join(psswd)

def part2(psswd):
	psswd = list(part1(psswd))
	increment_pass(psswd)
	return part1(psswd)

