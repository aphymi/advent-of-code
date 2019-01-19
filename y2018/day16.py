from util.parse import *


def separate_insts(int_lines):
	samples = []
	
	for ln in range(0, len(int_lines), 4):
		if not int_lines[ln]:
			break
		
		samples.append((int_lines[ln], int_lines[ln + 1], int_lines[ln + 2]))
	
	insts = int_lines[ln + 2:]
	
	return (samples, insts)


parse_input = compose(separate_insts, get_ints)

# I didn't want to put these all out specifically. I really didn't.
# I tried to use lambda functions in a for loop, but apparently
#   lambdas don't preserve the scope they were created in.
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
	rs[c] = op(rs, a, b)

def similars(sample):
	bef, inp, aft = sample
	sims = set()
	for opn, op in ops.items():
		work = bef.copy()
		apply(work, op, inp[1:])
		if work == aft:
			sims.add(opn)
	
	return sims

def part1(inp):
	samples, _ = inp
	
	return sum(1 if len(similars(sample)) >= 3 else 0 for sample in samples)

def part2(inp):
	samples, insts = inp
	
	opcodes = [set(ops.keys()) for _ in range(16)]
	
	# Find each opcode's function
	for sample in samples:
		opcodes[sample[1][0]] &= similars(sample)
	
	found = set()
	while len(found) < len(opcodes):
		for i, opc_posses in enumerate(opcodes):
			if not isinstance(opc_posses, set):
				continue
			if len(opc_posses) == 1:
				opcodes[i] = opc_posses.pop()
				found.add(opcodes[i])

			else:
				opcodes[i] -= found

	rs = [0, 0, 0, 0]
	for inst in insts:
		apply(rs, ops[opcodes[inst[0]]], inst[1:])
	
	return rs[0]
