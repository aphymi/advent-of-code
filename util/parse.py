import re

def compose(*ops):
	ops = reversed(ops)
	
	def composed(inp):
		for op in ops:
			inp = op(inp)
		return inp
	
	return composed

def parallel(*ops):
	def paralleled(inp):
		return list(zip(*[op(inp) for op in ops]))
	
	return paralleled

def split(lines):
	return [line.split() for line in lines]

def split_on(spl=None):
	def splitted(lines):
		return [line.split(spl) for line in lines]
	
	return splitted

def map_func(func):
	def mapped(inp):
		return [func(line) for line in inp]
	
	return mapped

def single_line(lines):
	return lines[0]

def get_regex_matches(regex):
	def get_matches(lines):
		return [re.findall(regex, line) for line in lines]
	
	return get_matches

def get_ints(lines):
	return [[int(m) for m in line] for line in get_regex_matches(r"-?\d+")(lines)]

def get_pos_ints(lines):
	return [[int(m) for m in line] for line in get_regex_matches(r"\d+")(lines)]
