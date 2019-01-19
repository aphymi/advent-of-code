from util.parse import *
parse_input = single_line

def say(look):
	said = [[look[0], 1]]
	for c in look[1:]:
		if c == said[-1][0]:
			said[-1][1] += 1
			
		else:
			said[-1][1] = said[-1][1]
			said.append([c, 1])
	
	return said

def iterate_las(look, times):
	for _ in range(times):
		look = "".join(str(freq) + c for c, freq in say(look))
	
	return look
	
	
def part1(look):
	return len(iterate_las(look, 40))

def part2(look):
	return len(iterate_las(look, 50))
