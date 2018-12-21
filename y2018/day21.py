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
	t = 0
	while 0 <= rs[ipr] < len(insts):
		if rs[ipr] == 28:
			print(rs)
		apply(rs, *insts[rs[ipr]])
		rs[ipr] += 1
		t += 1
	
	return t

def part1(inp):
	ipr, insts = inp
	
	# Can tell by analysis of the program that the value in r0 matters in exactly one case.
	#   If it's equal to the value of r4 at instruction 28, the program halts. Otherwise, it continues.
	#   Since r4 only ever gets bigger as the program goes on, the value of r4 at the very first execution
	#   of instruction 28 is the value we're looking for.
	
	rs = [0]*6
	while rs[ipr] != 28:
		apply(rs, *insts[rs[ipr]])
		rs[ipr] += 1
	
	return rs[4]

def part2(inp):
	ipr, insts = inp
	
	rs = [0]*6
	seen = set()
	prev = None
	while True:
		if rs[ipr] == 28:
			if rs[4] in seen:
				return prev
			seen.add(rs[4])
			prev = rs[4]
		apply(rs, *insts[rs[ipr]])
		rs[ipr] += 1
