import re

def part1(lines):
	def chars_in_mem(string):
		return len(re.findall(r"\\(?:[\\\"]|x\w\w)|\w", string[1:-1]))
	
	return sum([len(line) - chars_in_mem(line) for line in lines])

def part2(lines):
	def chars_in_enc(string):
		return len(string) + string.count("\\") + string.count("\"") + 2
	
	return sum([chars_in_enc(line) - len(line) for line in lines])
