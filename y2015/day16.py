from util.parse import *

def sue_info(line):
	colon_ind = line.index(":")
	sue_num = line[4:colon_ind]
	
	attrs_str = line[colon_ind+2:]
	
	attrs = {k: int(v) for k, v in (attr.split(": ") for attr in attrs_str.split(", "))}
	
	return (sue_num, attrs)

parse_input = map_func(sue_info)


FACTS = {
	"children": 3,
	"cats": 7,
	"samoyeds": 2,
	"pomeranians": 3,
	"akitas": 0,
	"vizslas": 0,
	"goldfish": 5,
	"trees": 3,
	"cars": 2,
	"perfumes": 1,
}

def part1(sues):
	for sue_num, attrs in sues:
		if all(v == FACTS[k] for k, v in attrs.items()):
			return sue_num

def part2(sues):
	def matches(key, value):
		if key in ("cats", "trees"):
			return value > FACTS[key]
		
		elif key in ("pomeranians", "goldfish"):
			return value < FACTS[key]
		
		else:
			return value == FACTS[key]
	
	for sue_num, attrs in sues:
		if all(matches(k, v) for k, v in attrs.items()):
			return sue_num
