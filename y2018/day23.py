import z3

from util.parse import *
parse_input = compose(map_func(lambda l: (l[:3], l[3])), get_ints)


def m_dist(pos1, pos2):
	return sum(abs(c1 - c2) for c1, c2 in zip(pos1, pos2))


def part1(nanobots):
	strong = max(nanobots, key=lambda n: n[1])
	
	return len([nb for nb in nanobots if m_dist(strong[0], nb[0]) <= strong[1]])

def part2(nanobots):
	# New library! Let's learn z3!
	
	optimiser = z3.Optimize()
	
	def z3_abs(x):
		return z3.If(x >= 0, x, -x)
	
	def z3_mdist(pos1, pos2):
		return z3_abs(pos1[0]-pos2[0]) + z3_abs(pos1[1]-pos2[1]) + z3_abs(pos1[2]-pos2[2])
	
	cand = tuple(map(z3.Int, "xyz"))
	
	near_bots = sum(z3.If(z3_mdist(cand, pos) <= rad, 1, 0) for pos, rad in nanobots)
	optimiser.maximize(near_bots)
	# Get the one closest to 0, 0, 0.
	optimiser.minimize(z3_mdist(cand, (0, 0, 0)))
	
	optimiser.check()
	
	model = optimiser.model()
	
	return m_dist((0, 0, 0), map(lambda c: model[c].as_long(), cand))
