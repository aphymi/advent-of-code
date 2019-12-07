from util.parse import *
from y2019 import intcode

parse_input = compose(get_ints, single_line)

def part1(program: intcode.IntcodeProgram) -> int:
	program = program[:]
	outputs = intcode.run_program_to_completion(
		program,
		inputs=[1],
	)
	
	return outputs[-1]

def part2(program: intcode.IntcodeProgram) -> int:
	program = program[:]
	outputs = intcode.run_program_to_completion(
		program,
		inputs=[5],
	)
	
	return outputs[-1]
