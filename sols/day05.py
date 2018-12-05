from functools import reduce
from string import ascii_lowercase

def preprocess_input(lines):
	# Only one line
	return lines[0]

def react(units):
	def app_ret(lst, elem):
		lst.append(elem)
		return lst
	
	def pop_ret(lst):
		lst.pop()
		return lst

	return reduce(lambda so_far, elem: app_ret(so_far, elem) if not so_far
										else (pop_ret(so_far) if elem.swapcase() == so_far[-1]
												else app_ret(so_far, elem)),
					units, [])

def part1(units):
	return len(react(units))

def part2(units):
	# Get a list of (character, len of reactted chain without character)
	lens = [len(react([c for c in units if c not in (o, o.upper())]))
			for o in ascii_lowercase]
	return min(lens)

