import re

def part1(lines):
	def nice(line):
		return sum([line.count(v) for v in "aeiou"]) >= 3 and \
				re.search(r"(.)\1", line) and \
				all([bad not in line for bad in ("ab", "cd", "pq", "xy")])
	
	return sum([1 if nice(line) else 0 for line in lines])

def part2(lines):
	def nice(line):
		return re.search(r"(..).*\1", line) and re.search(r"(.).\1", line)
	
	return sum([1 if nice(line) else 0 for line in lines])
