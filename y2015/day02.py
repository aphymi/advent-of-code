from functools import reduce
import re

def preprocess_input(lines):
	dims = []
	for line in lines:
		dims.append(map(int, re.findall("\d+", line)))
	
	return dims

def part1(dims):
	def paper(dim):
		l, w, h = dim
		sas = [l*w, w*h, l*h]
		return 2*sum(sas) + min(sas)


	return reduce(lambda s, dim: s+paper(dim), dims, 0)

def part2(dims):
	def ribbon(dim):
		l, w, h = dim
		return 2*min(l+w, w+h, l+h) + l*w*h
	
	return reduce(lambda s, dim: s+ribbon(dim), dims, 0)

