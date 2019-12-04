from util.parse import *
from y2019 import intcode

parse_input = compose(single_line, get_ints)

def part1(program):
	program = program[:] # Make a copy.
	program[1] = 12
	program[2] = 2
	
	intcode.run_program_to_completion(program)
	
	return program[0]

def part2(program):
	
	for i in range(0, 100):
		for j in range(0, 100):
			new_program = program[:] # Make a copy.
			
			new_program[1] = i
			new_program[2] = j
			
			intcode.run_program_to_completion(new_program)
			
			if new_program[0] == 19690720:
				return (100 * i) + j
	
	raise Exception("No valid noun and verb found")
