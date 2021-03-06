from functools import reduce
from string import ascii_lowercase

from util.parse import *
parse_input = single_line

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
	# Reacting the full chain before filtering letters individually will do a bunch of work upfront
	#   without affecting the result, and so save a lot of time during the a-z iteration.
	reacted_units = react(units)
	
	return min([len(react([c for c in reacted_units if c not in (o, o.upper())]))
					for o in ascii_lowercase])
