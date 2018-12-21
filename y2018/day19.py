from math import ceil, sqrt

def preprocess_input(lines):
	insts = []
	ipr = None
	for line in lines:
		if line.startswith("#"):
			ipr = int(line[4])
		else:
			s = line.split()
			insts.append((s[0], list(map(int, s[1:]))))
	
	return (ipr, insts)


ops = {
	"addr": lambda rs, a, b: rs[a] + rs[b],
	"addi": lambda rs, a, b: rs[a] + b,
	
	"mulr": lambda rs, a, b: rs[a] * rs[b],
	"muli": lambda rs, a, b: rs[a] * b,
	
	"banr": lambda rs, a, b: rs[a] & rs[b],
	"bani": lambda rs, a, b: rs[a] & b,
	
	"borr": lambda rs, a, b: rs[a] | rs[b],
	"bori": lambda rs, a, b: rs[a] | b,
	
	"setr": lambda rs, a, _: rs[a],
	"seti": lambda rs, a, _: a,
	
	"gtir": lambda rs, a, b: 1 if a > rs[b] else 0,
	"gtri": lambda rs, a, b: 1 if rs[a] > b else 0,
	"gtrr": lambda rs, a, b: 1 if rs[a] > rs[b] else 0,
	
	"eqir": lambda rs, a, b: 1 if a == rs[b] else 0,
	"eqri": lambda rs, a, b: 1 if rs[a] == b else 0,
	"eqrr": lambda rs, a, b: 1 if rs[a] == rs[b] else 0,
}

def apply(rs, op, inp):
	a, b, c = inp
	rs[c] = ops[op](rs, a, b)

def run_program(ipr, insts, rs):
	# Preserved for posterity.
	
	while 0 <= rs[ipr] < len(insts):
		apply(rs, *insts[rs[ipr]])
		rs[ipr] += 1
	
	return rs[0]

def calc_solution(ipr, insts, rs):
	# This requires the insight that the program is calculating the sum of all factors of a value.
	while rs[1] == 0:
		apply(rs, *insts[rs[ipr]])
		rs[ipr] += 1
	
	factors = set()
	for x in range(1, ceil(sqrt(rs[2]))+1):
		d, m = divmod(rs[2], x)
		if m == 0:
			factors.add(x)
			factors.add(d)
	
	return sum(factors)

def part1(inp):
	return calc_solution(*inp, [0]*6)

def part2(inp):
	rs = [0]*6
	rs[0] = 1
	
	return calc_solution(*inp, rs)
