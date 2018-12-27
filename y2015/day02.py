import re

def preprocess_input(lines):
	dims = []
	for line in lines:
		dims.append(list(map(int, re.findall("\d+", line))))
	
	return dims

def part1(dims):
	def paper(dim):
		l, w, h = dim
		sas = [l*w, w*h, l*h]
		return 2*sum(sas) + min(sas)

	return sum(paper(dim) for dim in dims)

def part2(dims):
	def ribbon(dim):
		l, w, h = dim
		return 2*min(l+w, w+h, l+h) + l*w*h
	
	return sum(ribbon(dim) for dim in dims)

