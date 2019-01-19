def parse_input(lines):
	ipr = int(lines[0][4:])

	insts = []
	for line in lines[1:]:
		s = line.split()
		insts.append((s[0], [int(n) for n in s[1:]]))
	
	eq_inst = None
	for inst in insts:
		if inst[0] == "eqrr":
			eq_inst = inst
			break
	
	return (eq_inst[1][0] or eq_inst[1][1], ipr, insts)


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

def part1(inp):
	eqr, ipr, insts = inp
	
	# Can tell by analysis of the program that the value in r0 matters in exactly one case.
	#   If it's equal to the value of r4 at instruction 28, the program halts. Otherwise, it continues.
	#   Since r4 only ever gets bigger as the program goes on, the value of r4 at the very first execution
	#   of instruction 28 is the value we're looking for.
	
	rs = [0]*6
	while rs[ipr] != 28:
		apply(rs, *insts[rs[ipr]])
		rs[ipr] += 1
	
	return rs[eqr]

def part2(inp):
	eqr, ipr, insts = inp
	
	rs = [0]*6
	seen = set()
	prev = None
	while True:
		if rs[ipr] == 28:
			if rs[eqr] in seen:
				return prev
			seen.add(rs[eqr])
			prev = rs[eqr]
		apply(rs, *insts[rs[ipr]])
		rs[ipr] += 1
