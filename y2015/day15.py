from util.parse import *
parse_input = get_ints

def recs(rem_recs, rem_spots):
	for num in range(rem_spots + 1):
		if rem_recs:
			for orecs in recs(rem_recs - 1, rem_spots - num):
				yield [num] + orecs
		else:
			yield [num]

def score(recipes, distrib):
	p = 1
	z_recs = list(zip(recipes, distrib))
	for m in range(len(recipes[0]) - 1):
		p *= max(sum(r[m] * d for r, d in z_recs), 0)
	
	return p


def part1(recipes):
	return max(score(recipes, distrib) for distrib in recs(len(recipes)-1, 100))

def part2(recipes):
	def cals(recipes, distrib):
		return sum(r[4] * d for r, d in zip(recipes, distrib))
	
	return max(score(recipes, distrib) for distrib in recs(len(recipes)-1, 100) if cals(recipes, distrib) == 500)
